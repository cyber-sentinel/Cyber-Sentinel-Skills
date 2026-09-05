import copy
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from cskills.checks import check_handler_surface, validate_repository
from cskills.runtime import authorize, run
from cskills.validation import (MAX_BYTES, ROOT, Rejected, bounded_path, check_schema,
                                check_secret_surface, decode_json, load_manifest,
                                manifests, parse_frontmatter, read_json, validate_data)
from tests.common import MANIFEST_PATH, RepositoryCopy, fixture


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.skill, self.data, _ = fixture('summarize-evidence')
        self.manifest = read_json(ROOT, MANIFEST_PATH)

    def test_every_required_contract_field_is_enforced(self):
        schema = read_json(ROOT, 'schemas/skill-contract.schema.json')
        for key in self.manifest:
            with self.subTest(field=key), self.assertRaises(Rejected):
                altered = copy.deepcopy(self.manifest)
                del altered[key]
                validate_data(altered, schema)

    def test_unknown_contract_and_malformed_semver_fail(self):
        schema = read_json(ROOT, 'schemas/skill-contract.schema.json')
        for version in ['1', '1.0', '01.0.0', '1.00.0', '1.0.0-01', '1.0.0-', '0.1.0\n']:
            with self.subTest(version=version), self.assertRaises(Rejected):
                altered = {**self.manifest, 'version': version}
                validate_data(altered, schema)
        with self.assertRaises(Rejected):
            validate_data({**self.manifest, 'contract_version': '9.0.0'}, schema)

    def test_valid_semver_prerelease_and_build_metadata(self):
        schema = read_json(ROOT, 'schemas/skill-contract.schema.json')
        for version in ['0.1.0', '1.2.3-rc.1', '1.2.3+build.1', '1.2.3-0+build']:
            validate_data({**self.manifest, 'version': version}, schema)

    def test_newline_suffix_is_not_part_of_a_stable_identifier(self):
        schema = read_json(ROOT, 'schemas/skill-contract.schema.json')
        for key in ['id', 'name']:
            with self.subTest(field=key), self.assertRaises(Rejected):
                validate_data({**self.manifest, key: self.manifest[key] + '\n'}, schema)
        self.data['sources'][0]['id'] += '\n'
        self.data['claims'][0]['source_ids'] = [self.data['sources'][0]['id']]
        with self.assertRaisesRegex(Rejected, 'schema-rejected'):
            run(self.skill, self.data)

    def test_duplicate_json_keys_nonfinite_and_deep_json_rejected(self):
        for data in [b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}',
                     b'{"a":1e999}', b'[' * 40 + b'0' + b']' * 40, b'\xff']:
            with self.subTest(data=data[:20]), self.assertRaises(Rejected):
                decode_json(data)

    def test_byte_limit_is_checked_before_json_parsing(self):
        with self.assertRaisesRegex(Rejected, 'byte-limit'):
            decode_json(b' ' * (MAX_BYTES + 1))

    def test_remote_file_and_dynamic_schema_references_rejected(self):
        for key in ['$ref', '$dynamicRef']:
            for ref in ['https://example.invalid/schema', 'file:///etc/passwd', '../schema.json', '#anchor']:
                with self.subTest(key=key, ref=ref), self.assertRaises(Rejected):
                    check_schema({key: ref})

    def test_missing_local_schema_reference_is_rejected_without_retrieval(self):
        with self.assertRaisesRegex(Rejected, 'schema-evaluation-failed'):
            validate_data({}, {'$ref': '#/missing'})

    def test_local_fragment_reference_works_offline(self):
        validate_data('ok', {'$defs': {'text': {'type': 'string'}}, '$ref': '#/$defs/text'})

    def test_forged_llm_grants_are_not_accepted_as_inputs(self):
        self.data['approved_by_user'] = True
        self.data['permissions'] = {'shell': True}
        with self.assertRaises(Rejected):
            run(self.skill, self.data)

    def test_unknown_skill_rejected(self):
        with self.assertRaisesRegex(Rejected, 'unknown-skill'):
            run('cs.skills.research.unknown', self.data)

    def test_all_side_effect_capabilities_fail_even_if_claimed_authorized(self):
        for capability in ['WRITE', 'EXECUTE', 'DESTRUCTIVE']:
            with self.subTest(capability=capability), self.assertRaises(Rejected):
                manifest = copy.deepcopy(self.manifest)
                manifest['permissions']['capabilities'].append(capability)
                manifest['safety']['authorization_policy'] = 'explicit-user-authorization'
                authorize(manifest)

    def test_network_scope_tools_services_filesystem_and_privileges_fail(self):
        mutations = [
            lambda m: m['permissions']['network'].update(enabled=True, hosts=['example.com']),
            lambda m: m['permissions']['network'].update(hosts=['example.com']),
            lambda m: m['permissions']['filesystem']['read'].append('input'),
            lambda m: m['permissions']['filesystem']['write'].append('output'),
            lambda m: m['permissions'].update(shell=True),
            lambda m: m['permissions'].update(privilege_escalation=True),
            lambda m: m['permissions']['environment'].append('EXAMPLE_SETTING'),
            lambda m: m['permissions']['external_services'].append({'name': 'external', 'hosts': ['example.com']}),
            lambda m: m['required_tools'].append({'name': 'curl', 'version': '1.0.0'}),
            lambda m: m['dependencies'].append({'id': 'other', 'version': '1.0.0'}),
            lambda m: m['side_effects'].append({'capability': 'WRITE', 'description': 'An output file'}),
            lambda m: m['execution'].update(source_content_execution=True),
            lambda m: m['execution'].update(kind='adapter'),
            lambda m: m['execution']['ai'].update(required=True, providers=['provider']),
        ]
        for n, mutate in enumerate(mutations):
            with self.subTest(case=n), self.assertRaises(Rejected):
                manifest = copy.deepcopy(self.manifest)
                mutate(manifest)
                authorize(manifest)

    def test_unknown_handler_cannot_be_loaded_from_a_path(self):
        for field, value in [('id', 'cs.skills.research.unknown'),
                             ('name', 'another-name')]:
            with self.subTest(field=field), self.assertRaises(Rejected):
                authorize({**self.manifest, field: value})
        altered = copy.deepcopy(self.manifest)
        altered['execution']['entrypoint'] = 'os.system'
        with self.assertRaises(Rejected):
            authorize(altered)

    def test_missing_manifest_and_unknown_metadata_fail_closed(self):
        with RepositoryCopy() as repo:
            (repo.root / MANIFEST_PATH).unlink()
            with self.assertRaises(Rejected):
                run(self.skill, self.data, repo.root)
        with RepositoryCopy() as repo:
            repo.mutate(MANIFEST_PATH, lambda m: m.update(unknown_setting=True))
            with self.assertRaises(Rejected):
                run(self.skill, self.data, repo.root)

    def test_duplicate_stable_skill_id_rejected(self):
        with RepositoryCopy() as repo:
            other = 'skills/incident-response/build-timeline/skill.json'
            repo.mutate(other, lambda m: m.update(id=self.skill))
            with self.assertRaisesRegex(Rejected, 'duplicate-skill-id'):
                manifests(repo.root)

    def test_paths_reject_traversal_absolute_windows_and_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            for path in ['../outside.json', '/etc/passwd', 'C:/secret.json',
                         'a\\b', 'a//b', './file', 'a/../b', '']:
                with self.subTest(path=path), self.assertRaises(Rejected):
                    bounded_path(Path(directory), path)
            target = Path(directory) / 'target'
            target.write_text('{}', encoding='utf-8')
            link = Path(directory) / 'link'
            try:
                link.symlink_to(target)
            except OSError:
                return  # Some Windows hosts do not grant symlink creation.
            with self.assertRaisesRegex(Rejected, 'symlink-path'):
                bounded_path(Path(directory), 'link')

    @unittest.skipUnless(os.name == 'nt', 'Windows junction-specific boundary')
    def test_windows_junction_cannot_escape_selected_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'scope'
            outside = Path(directory) / 'outside'
            root.mkdir()
            outside.mkdir()
            (outside / 'input.json').write_text('{}', encoding='utf-8')
            junction = root / 'junction'
            created = subprocess.run(['cmd', '/c', 'mklink', '/J', str(junction), str(outside)],
                                     capture_output=True, timeout=10)
            self.assertEqual(created.returncode, 0, 'Could not create synthetic junction')
            try:
                with self.assertRaises(Rejected):
                    bounded_path(root, 'junction/input.json')
            finally:
                junction.rmdir()

    def test_frontmatter_duplicates_tags_aliases_and_drift_rejected(self):
        for text in ['---\nname: "a"\nname: "a"\n---\nbody',
                     '---\nname: &anchor a\ndescription: *anchor\n---\nbody',
                     '---\nname: !!python/object:bad\ndescription: "b"\n---\nbody']:
            with self.assertRaises(Rejected):
                parse_frontmatter(text)
        with RepositoryCopy() as repo:
            repo.mutate(MANIFEST_PATH, lambda m: m.update(description='Different text'))
            with self.assertRaisesRegex(Rejected, 'frontmatter-manifest-mismatch'):
                manifests(repo.root)

    def test_secret_fields_values_and_sensitive_filenames_rejected(self):
        field = 'pass' + 'word'
        values = [{field: 'synthetic-only'}, 'gh' + 'p_' + 'A' * 36,
                  'AK' + 'IA' + 'A' * 16, 'Bearer' + ' ' + 'A' * 20,
                  '-----BEGIN ' + 'PRIVATE KEY-----', 'https://' + 'user:synthetic' + '@example.com/']
        for value in values:
            with self.assertRaises(Rejected):
                check_secret_surface(value)
        with RepositoryCopy() as repo:
            (repo.root / '.env').write_text('synthetic', encoding='utf-8')
            with self.assertRaisesRegex(Rejected, 'sensitive-filename'):
                validate_repository(repo.root)

    def test_unknown_executable_skill_resource_rejected(self):
        with RepositoryCopy() as repo:
            (repo.root / MANIFEST_PATH).parent.joinpath('helper.py').write_text('print(1)\n')
            with self.assertRaisesRegex(Rejected, 'undeclared-or-missing-skill-file'):
                validate_repository(repo.root)

    def test_undeclared_network_import_in_handler_rejected(self):
        with RepositoryCopy() as repo:
            path = repo.root / 'cskills/handlers.py'
            path.write_text(path.read_text(encoding='utf-8') + '\nimport socket\n', encoding='utf-8')
            with self.assertRaisesRegex(Rejected, 'undeclared-handler-import'):
                check_handler_surface(repo.root)

    def test_broken_local_documentation_link_rejected(self):
        with RepositoryCopy() as repo:
            path = repo.root / 'README.md'
            path.write_text(path.read_text(encoding='utf-8') + '\n[Missing](missing.md)\n', encoding='utf-8')
            with self.assertRaisesRegex(Rejected, 'broken-documentation-link'):
                validate_repository(repo.root)
