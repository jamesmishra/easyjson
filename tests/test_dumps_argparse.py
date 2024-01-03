import argparse
import unittest

import easyjson


class TestDumpsArgparse(unittest.TestCase):

    def test_simple(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument("--some-random-flag", type=int)
        parser.add_argument("--other-flag", type=str)
        obj = parser.parse_args([
            "--some-random-flag", "1",
            "--other-flag", "2",
        ])
        actual = easyjson.dumps(obj, sort_keys=True)
        expected = '{"other_flag": "2", "some_random_flag": 1}'
        self.assertEqual(expected, actual)
