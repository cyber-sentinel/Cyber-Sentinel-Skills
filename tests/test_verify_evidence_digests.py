# Copyright (c) 2026 Ali RahimDabagh
# SPDX-License-Identifier: Apache-2.0

import base64
import copy
import hashlib
import unittest

from cskills.runtime import run
from cskills.validation import ROOT, Rejected, read_json
from tests.common import fixture


class EvidenceDigestTests(unittest.TestCase):
    def setUp(self):
        self.skill, self.data, self.expected = fixture('verify-evidence-digests')

    def test_matching_fixture_sorted_and_reproducible(self):
        first = run(self.skill, self.data)
        self.assertEqual(first['result'], self.expected)
        self.assertEqual(first, run(self.skill, copy.deepcopy(self.data)))
        self.assertEqual([item['id'] for item in first['result']['items']], ['a', 'b'])
        self.assertNotIn('content_base64', str(first['result']))

    def test_mismatch_is_a_result_not_an_execution_error(self):
        folder = 'skills/incident-response/verify-evidence-digests/examples'
        data = read_json(ROOT, folder + '/mismatch-input.json')
        expected = read_json(ROOT, folder + '/mismatch-expected.json')
        self.assertEqual(run(self.skill, data)['result'], expected)

    def test_empty_bytes_are_hashed_without_special_casing(self):
        item = self.data['items'][0]
        item['content_base64'] = ''
        item['expected_sha256'] = hashlib.sha256(b'').hexdigest()
        result = run(self.skill, self.data)['result']['items'][1]
        self.assertEqual(result['byte_length'], 0)
        self.assertTrue(result['matches'])

    def test_invalid_and_noncanonical_base64_fail_closed(self):
        for value in ['****', 'Zg', 'Zg===', 'Zh==', 'Zg==\n', 'Zg==junk']:
            with self.subTest(value=value), self.assertRaises(Rejected):
                self.data['items'][0]['content_base64'] = value
                run(self.skill, self.data)

    def test_decoded_limit_and_item_count_are_enforced(self):
        item = self.data['items'][0]
        item['content_base64'] = base64.b64encode(b'x' * 65536).decode('ascii')
        item['expected_sha256'] = hashlib.sha256(b'x' * 65536).hexdigest()
        self.assertEqual(run(self.skill, self.data)['result']['items'][1]['byte_length'], 65536)
        item['content_base64'] = base64.b64encode(b'x' * 65537).decode('ascii')
        with self.assertRaisesRegex(Rejected, 'evidence-byte-limit'):
            run(self.skill, self.data)
        item['content_base64'] = 'eA=='
        self.data['items'] = [copy.deepcopy(self.data['items'][0]) for _ in range(11)]
        with self.assertRaisesRegex(Rejected, 'schema-rejected'):
            run(self.skill, self.data)

    def test_duplicate_id_unknown_source_and_bad_digest_rejected(self):
        self.data['items'][1]['id'] = self.data['items'][0]['id']
        with self.assertRaisesRegex(Rejected, 'duplicate-record-id'):
            run(self.skill, self.data)
        self.data['items'][1]['id'] = 'a'
        self.data['items'][1]['source_ids'] = ['unknown']
        with self.assertRaisesRegex(Rejected, 'missing-source-reference'):
            run(self.skill, self.data)
        self.data['items'][1]['source_ids'] = ['s1']
        self.data['items'][1]['expected_sha256'] = 'A' * 64
        with self.assertRaisesRegex(Rejected, 'schema-rejected'):
            run(self.skill, self.data)

    def test_encoded_known_secret_pattern_is_rejected_without_payload_echo(self):
        sample = 'pass' + 'word=' + 'synthetic-marker'
        self.data['items'][0]['content_base64'] = base64.b64encode(sample.encode()).decode()
        with self.assertRaisesRegex(Rejected, '^secret-like-value$'):
            run(self.skill, self.data)
