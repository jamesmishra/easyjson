import unittest
from typing import FrozenSet, Set

import easyjson


class TestDumpsDatetime(unittest.TestCase):

    def test_set_empty(self) -> None:
        obj: Set[int] = set()
        actual = easyjson.dumps(obj)
        expected = '[]'
        self.assertEqual(expected, actual)

    def test_frozenset_empty(self) -> None:
        obj: FrozenSet[int] = frozenset()
        actual = easyjson.dumps(obj)
        expected = '[]'
        self.assertEqual(expected, actual)

    def test_set_simple(self) -> None:
        obj = set([1, 2, 3])
        actual = easyjson.dumps(obj)
        expected = '[1, 2, 3]'
        self.assertEqual(expected, actual)

    def test_frozenset_simple(self) -> None:
        obj = set([1, 2, 3])
        actual = easyjson.dumps(obj)
        expected = '[1, 2, 3]'
        self.assertEqual(expected, actual)

    def test_set_nested(self) -> None:
        obj = set([1, 2, frozenset([4, 5, 6])])
        actual = easyjson.dumps(obj)
        expected = '[1, 2, [4, 5, 6]]'
        self.assertEqual(expected, actual)
