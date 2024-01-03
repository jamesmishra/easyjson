import unittest

import easyjson


class TestDumpBytes(unittest.TestCase):

    def test_simple(self) -> None:
        obj = b"abcd 1234!"
        actual = easyjson.dumps(obj)
        expected = '"YWJjZCAxMjM0IQ=="'
        self.assertEqual(expected, actual)

    def test_empty_string(self) -> None:
        obj = b""
        actual = easyjson.dumps(obj)
        expected = '""'
        self.assertEqual(expected, actual)
