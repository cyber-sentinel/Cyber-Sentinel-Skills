import unittest

from cskills.runtime import run
from cskills.validation import Rejected
from tests.common import fixture


class DetectionTests(unittest.TestCase):
    def setUp(self):
        self.skill, self.data, self.expected = fixture('review-detection-spec')

    def test_incomplete_spec_reports_actionable_gaps(self):
        self.assertEqual(run(self.skill, self.data)['result'], self.expected)

    def test_explicit_vendor_backend_labels_remain_distinct(self):
        for backend in ['microsoft-kql', 'elastic-kql', 'elastic-eql', 'elastic-esql', 'splunk-spl', 'sigma']:
            with self.subTest(backend=backend):
                self.data['rule']['backend'] = backend
                self.assertEqual(run(self.skill, self.data)['result']['backend'], backend)

    def test_ambiguous_kql_and_unknown_backends_rejected(self):
        for backend in ['kql', 'KQL', 'sql', 'unknown']:
            with self.subTest(backend=backend), self.assertRaises(Rejected):
                self.data['rule']['backend'] = backend
                run(self.skill, self.data)

    def test_complete_metadata_does_not_certify_query_correctness(self):
        self.data['rule'].update({'log_sources': ['synthetic-events'], 'time_window_minutes': 15,
                                  'test_source_ids': ['s1'], 'false_positive_notes': 'Expected test traffic',
                                  'expression': 'Intentionally not valid query syntax'})
        result = run(self.skill, self.data)['result']
        self.assertTrue(result['metadata_complete'])
        self.assertEqual(result['findings'], [])
        self.assertNotIn('expression', result)
        self.assertIn('not evaluated', result['limitations'][0])

    def test_test_evidence_must_reference_a_known_source(self):
        self.data['rule']['test_source_ids'] = ['missing']
        with self.assertRaises(Rejected):
            run(self.skill, self.data)

    def test_zero_and_boolean_windows_rejected(self):
        for value in [0, -1, True]:
            with self.subTest(value=value), self.assertRaises(Rejected):
                self.data['rule']['time_window_minutes'] = value
                run(self.skill, self.data)
