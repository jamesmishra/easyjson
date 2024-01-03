import datetime
import unittest

import easyjson


class TestDumpsDatetime(unittest.TestCase):

    def test_simple(self) -> None:
        obj = datetime.date(year=2020, month=2, day=29)
        actual = easyjson.dumps(obj)
        expected = '"2020-02-29"'
        self.assertEqual(expected, actual)
