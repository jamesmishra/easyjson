import unittest

import easyjson
from tests.fixtures import dt_stamp


class TestDumpsDatetime(unittest.TestCase):

    def test_simple(self) -> None:
        actual = easyjson.dumps(dt_stamp)
        expected = '"2023-10-15T03:10:30.001234"'
        self.assertEqual(expected, actual)

    def test_in_list(self) -> None:
        obj = [
            1,
            2.0,
            dt_stamp,
            None,
        ]
        actual = easyjson.dumps(obj)
        expected = '[1, 2.0, "2023-10-15T03:10:30.001234", null]'
        self.assertEqual(expected, actual)
