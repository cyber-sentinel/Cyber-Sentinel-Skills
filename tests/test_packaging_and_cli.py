# Copyright (c) 2026 Ali RahimDabagh
# SPDX-License-Identifier: Apache-2.0

import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from cskills.packaging import build_bundle, verify_bundle
from cskills.checks import validate_repository
from cskills.validation import ROOT, Rejected, canonical
from tests.common import RepositoryCopy


class PackagingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = build_bundle()

    def test_review_bundle_is_byte_reproducible_and_verified(self):
        self.assertEqual(self.bundle, build_bundle())
        self.assertEqual(verify_bundle(self.bundle)['sha256'], hashlib.sha256(self.bundle).hexdigest())
        with zipfile.ZipFile(io.BytesIO(self.bundle)) as archive:
            manifest = json.loads(archive.read('BUNDLE-MANIFEST.json'))
            self.assertEqual(manifest['license_status'], 'approved')
            self.assertEqual(manifest['license'], 'Apache-2.0')
            self.assertEqual(manifest['purpose'], 'review-only')
            self.assertIn('schemas/skill-contract.schema.json', manifest['files'])
            self.assertIn('cskills/runtime.py', manifest['files'])
            self.assertNotIn('.git/config', manifest['files'])
            for name in ['LICENSE', 'NOTICE']:
                self.assertEqual(archive.read(name), (ROOT / name).read_bytes())

    def rewrite_legal_materials(self, replacements):
        # Recompute the inventory too: a matching file digest is insufficient
        # when a distributor has stripped the license or project attribution.
        output = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(self.bundle)) as source:
            contents = {info.filename: source.read(info) for info in source.infolist()}
            for name, content in replacements.items():
                if content is None:
                    del contents[name]
                else:
                    contents[name] = content
            manifest = json.loads(contents['BUNDLE-MANIFEST.json'])
            manifest['files'] = {name: hashlib.sha256(content).hexdigest()
                                 for name, content in contents.items()
                                 if name != 'BUNDLE-MANIFEST.json'}
            contents['BUNDLE-MANIFEST.json'] = canonical(manifest) + b'\n'
            with zipfile.ZipFile(output, 'w') as dest:
                for info in source.infolist():
                    if info.filename in contents:
                        dest.writestr(info, contents[info.filename])
        return output.getvalue()

    def test_bundle_rejects_removed_legal_files_even_with_matching_inventory(self):
        for name in ['LICENSE', 'NOTICE']:
            with self.subTest(file=name), self.assertRaisesRegex(Rejected, 'missing-license-materials'):
                verify_bundle(self.rewrite_legal_materials({name: None}))

    def test_bundle_rejects_changed_license_or_stripped_attribution_with_matching_digests(self):
        for name, content in [('LICENSE', b'a different license'),
                              ('NOTICE', b'Cyber-Sentinel-Skills\n')]:
            with self.subTest(file=name), self.assertRaises(Rejected):
                verify_bundle(self.rewrite_legal_materials({name: content}))

    def test_repository_rejects_missing_or_changed_legal_materials(self):
        for name, content in [('LICENSE', None), ('NOTICE', None),
                              ('LICENSE', b'a different license'),
                              ('NOTICE', b'Cyber-Sentinel-Skills\n')]:
            with self.subTest(file=name, missing=content is None), RepositoryCopy() as repo:
                if content is None:
                    (repo.root / name).unlink()
                else:
                    (repo.root / name).write_bytes(content)
                with self.assertRaises(Rejected):
                    validate_repository(repo.root)

    def altered_bundle(self, mode):
        output = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(self.bundle)) as source, zipfile.ZipFile(output, 'w') as dest:
            for info in source.infolist():
                content = source.read(info)
                if info.filename == 'README.md':
                    if mode == 'tamper':
                        content += b'changed'
                    if mode == 'traversal':
                        info.filename = '../README.md'
                    if mode == 'symlink':
                        info.external_attr = 0o120777 << 16
                dest.writestr(info, content)
        return output.getvalue()

    def test_content_tampering_path_traversal_and_symlinks_rejected(self):
        for mode in ['tamper', 'traversal', 'symlink']:
            with self.subTest(mode=mode), self.assertRaises(Rejected):
                verify_bundle(self.altered_bundle(mode))

    def test_malformed_archive_and_oversize_archive_rejected(self):
        for data in [b'not-a-zip', b'x' * (5 * 1024 * 1024 + 1)]:
            with self.assertRaises(Rejected):
                verify_bundle(data)

    def test_bundle_runs_without_original_checkout(self):
        # Only our just-created, verified bundle is extracted into an isolated temp
        # directory for this integration test. Public CLI offers no extraction.
        with tempfile.TemporaryDirectory() as directory:
            with zipfile.ZipFile(io.BytesIO(self.bundle)) as archive:
                archive.extractall(directory)
            result = subprocess.run([sys.executable, '-m', 'cskills', 'run',
                'cs.skills.threat-intelligence.normalize-iocs', '--workspace',
                'skills/threat-intelligence/normalize-iocs/examples', '--input', 'input.json'],
                cwd=directory, capture_output=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertEqual(json.loads(result.stdout)['result']['indicators'][0]['value'], 'example.com')


class CliTests(unittest.TestCase):
    def test_valid_example_command(self):
        result = subprocess.run([sys.executable, '-m', 'cskills', 'run',
            'cs.skills.incident-response.build-timeline', '--workspace',
            'skills/incident-response/build-timeline/examples', '--input', 'input.json'],
            cwd=ROOT, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(json.loads(result.stdout)['result']['events'][0]['id'], 'e1')

    def test_rejected_input_is_never_echoed_in_errors(self):
        marker = 'sensitive-synthetic-test-value'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.json'
            path.write_text(json.dumps({'pass' + 'word': marker}), encoding='utf-8')
            result = subprocess.run([sys.executable, '-m', 'cskills', 'run',
                'cs.skills.research.summarize-evidence', '--workspace', directory, '--input', 'input.json'],
                cwd=ROOT, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, b'')
        self.assertNotIn(marker.encode(), result.stderr)
        self.assertEqual(json.loads(result.stderr)['error'], 'secret-like-field')

    def test_approved_license_does_not_grant_public_release_approval(self):
        result = subprocess.run([sys.executable, '-m', 'cskills', 'release-check'],
                                cwd=ROOT, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stderr)['error'], 'release-owner-approval-pending')

    def test_packaging_never_overwrites_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'review.zip'
            path.write_bytes(b'existing-evidence')
            result = subprocess.run([sys.executable, '-m', 'cskills', 'package', '--output', str(path)],
                                    cwd=ROOT, capture_output=True, timeout=30)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(path.read_bytes(), b'existing-evidence')
