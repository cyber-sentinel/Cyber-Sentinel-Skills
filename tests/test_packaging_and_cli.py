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
from cskills.validation import ROOT, Rejected


class PackagingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = build_bundle()

    def test_review_bundle_is_byte_reproducible_and_verified(self):
        self.assertEqual(self.bundle, build_bundle())
        self.assertEqual(verify_bundle(self.bundle)['sha256'], hashlib.sha256(self.bundle).hexdigest())
        with zipfile.ZipFile(io.BytesIO(self.bundle)) as archive:
            manifest = json.loads(archive.read('BUNDLE-MANIFEST.json'))
            self.assertEqual(manifest['license_status'], 'pending-owner-approval')
            self.assertEqual(manifest['purpose'], 'review-only')
            self.assertIn('schemas/skill-contract.schema.json', manifest['files'])
            self.assertIn('cskills/runtime.py', manifest['files'])
            self.assertNotIn('.git/config', manifest['files'])

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

    def test_release_gate_reports_pending_license(self):
        result = subprocess.run([sys.executable, '-m', 'cskills', 'release-check'],
                                cwd=ROOT, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stderr)['error'], 'license-owner-approval-pending')

    def test_packaging_never_overwrites_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'review.zip'
            path.write_bytes(b'existing-evidence')
            result = subprocess.run([sys.executable, '-m', 'cskills', 'package', '--output', str(path)],
                                    cwd=ROOT, capture_output=True, timeout=30)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(path.read_bytes(), b'existing-evidence')
