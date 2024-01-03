import json
import unittest
from collections import OrderedDict, defaultdict


class TestJSONStdlibSuccesses(unittest.TestCase):

    def test_defaultdict_succeeds(self) -> None:
        obj = defaultdict(list)
        obj["a"] = [1,2,3]
        actual = json.dumps(obj, sort_keys=True)
        expected = '{"a": [1, 2, 3]}'
        self.assertEqual(expected, actual)


    def test_ordereddict_succeeds(self) -> None:
        obj = OrderedDict(a=1, b=2)
        actual = json.dumps(obj, sort_keys=True)
        expected = '{"a": 1, "b": 2}'
        self.assertEqual(expected, actual)
