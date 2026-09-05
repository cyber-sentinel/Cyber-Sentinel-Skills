import unittest

from cskills.runtime import run
from cskills.validation import Rejected
from tests.common import fixture


class TimelineTests(unittest.TestCase):
    def setUp(self):
        self.skill, self.data, self.expected = fixture('build-timeline')

    def test_offsets_sorted_and_original_timestamps_retained(self):
        self.assertEqual(run(self.skill, self.data)['result'], self.expected)

    def test_equal_instants_use_record_id_as_stable_tiebreak(self):
        self.data['events'][0]['timestamp'] = '2026-09-05T10:00:00Z'
        events = run(self.skill, self.data)['result']['events']
        self.assertEqual([e['id'] for e in events], ['e1', 'e2'])
        self.assertEqual(events[0]['timestamp_utc'], events[1]['timestamp_utc'])

    def test_invalid_naive_unknown_offset_and_leap_second_rejected(self):
        for timestamp in ['2026-09-05T10:00:00', '2026-09-05T10:00:00-00:00',
                          '2026-02-30T10:00:00Z', '2026-09-05T10:00:60Z',
                          '2026-09-05T10:00:00+00:99', '2026-09-05T10:00:00+24:00',
                          '2026-09-05T10:00:00.1234567Z', '0001-01-01T00:00:00+01:00']:
            with self.subTest(timestamp=timestamp), self.assertRaises(Rejected):
                self.data['events'][0]['timestamp'] = timestamp
                run(self.skill, self.data)

    def test_fractional_seconds_and_date_rollover(self):
        self.data['events'][0]['timestamp'] = '2026-09-05T00:30:00.123+01:00'
        first = run(self.skill, self.data)['result']['events'][0]
        self.assertEqual(first['timestamp_utc'], '2026-09-04T23:30:00.123000Z')

    def test_unknown_source_rejected(self):
        self.data['events'][0]['source_id'] = 'missing'
        with self.assertRaises(Rejected):
            run(self.skill, self.data)
