import unittest
from datetime import timedelta

import easyjson


class TestDumpsTimedelta(unittest.TestCase):

    def testzero_timedelta(self) -> None:
        obj = timedelta()
        actual = easyjson.dumps(obj)
        expected = '"Duration: 0 microseconds"'
        self.assertEqual(expected, actual)

    def test_days(self) -> None:
        obj = timedelta(days=3)
        actual = easyjson.dumps(obj)
        expected = '"Duration: 3 days"'
        self.assertEqual(expected, actual)

    def test_days_hours(self) -> None:
        obj = timedelta(days=3, hours=5)
        actual = easyjson.dumps(obj)
        expected = '"Duration: 3 days, 5 hours"'
        self.assertEqual(expected, actual)

    def test_hours(self) -> None:
        obj = timedelta(hours=5)
        actual = easyjson.dumps(obj)
        expected = '"Duration: 5 hours"'
        self.assertEqual(expected, actual)

    def test_days_hours_minutes_seconds_us(self) -> None:
        obj = timedelta(
            days=3,
            hours=5,
            minutes=31,
            seconds=58,
            microseconds=12345,
        )
        actual = easyjson.dumps(obj)
        expected = (
            '"Duration: 3 days, 5 hours, 31 minutes, '
            '58 seconds, 12345 microseconds"'
        )
        self.assertEqual(expected, actual)

    def test_negative_days_hours_minutes_seconds_us(self) -> None:
        obj = timedelta(
            days=3,
            hours=5,
            minutes=31,
            seconds=58,
            microseconds=12345,
        ) * -1
        actual = easyjson.dumps(obj)
        expected = (
            '"Duration: -4 days, 18 hours, 28 minutes, '
            '2 seconds, 987655 microseconds"'
        )
        self.assertEqual(expected, actual)
