# Copyright (c) 2026 Ali RahimDabagh
# SPDX-License-Identifier: Apache-2.0

import unittest

from cskills.runtime import run
from cskills.validation import Rejected
from tests.common import fixture


class IndicatorTests(unittest.TestCase):
    def setUp(self):
        self.skill, self.data, self.expected = fixture('normalize-iocs')

    def test_dedup_preserves_records_and_rejects_invalid_ipv4(self):
        self.assertEqual(run(self.skill, self.data)['result'], self.expected)

    def test_ipv6_is_compressed_and_hash_is_lowercase(self):
        self.data['indicators'] = [
            {'id': 'i1', 'type': 'ipv6', 'value': '2001:0db8:0:0::1', 'source_ids': ['s1']},
            {'id': 'i2', 'type': 'sha256', 'value': 'AB' * 32, 'source_ids': ['s1']},
        ]
        result = run(self.skill, self.data)['result']['indicators']
        self.assertEqual([r['value'] for r in result], ['2001:db8::1', 'ab' * 32])

    def test_provenance_unioned_across_duplicate_indicators(self):
        self.data['sources'].append({'id': 's2', 'title': 'Second synthetic source', 'uri': 'urn:fixture:s2'})
        self.data['indicators'][1]['source_ids'] = ['s2']
        result = run(self.skill, self.data)['result']['indicators'][0]
        self.assertEqual(result['source_ids'], ['s1', 's2'])

    def test_mismatched_type_zone_unicode_url_and_invalid_label_rejected(self):
        values = [('ipv4', '2001:db8::1'), ('ipv6', 'fe80::1%eth0'),
                  ('domain', 'éxample.com'), ('domain', 'https://example.com'),
                  ('domain', '-invalid.example'), ('sha256', 'a' * 63)]
        self.data['indicators'] = [
            {'id': f'i{n}', 'type': kind, 'value': value, 'source_ids': ['s1']}
            for n, (kind, value) in enumerate(values)
        ]
        result = run(self.skill, self.data)['result']
        self.assertEqual(result['indicators'], [])
        self.assertEqual(len(result['rejected']), len(values))

    def test_private_ip_normalized_without_reputation_claim(self):
        self.data['indicators'] = [{'id': 'i1', 'type': 'ipv4', 'value': '10.0.0.1', 'source_ids': ['s1']}]
        result = run(self.skill, self.data)['result']['indicators'][0]
        self.assertEqual(set(result), {'type', 'value', 'source_ids', 'record_ids'})

    def test_duplicate_id_rejected_before_normalizing(self):
        self.data['indicators'][1]['id'] = self.data['indicators'][0]['id']
        with self.assertRaises(Rejected):
            run(self.skill, self.data)
