import unittest

import easyjson
from tests.fixtures import ComplexDataclass, SimpleDataclass, UnserializableDataclass


class TestDumpsDataclass(unittest.TestCase):

    def test_simple_1(self) -> None:
        obj = SimpleDataclass("a", 10, 100.0, None)
        actual = easyjson.dumps(obj, sort_keys=True)
        expected = '{"a": "a", "b": 10, "c": 100.0, "d": null}'
        self.assertEqual(expected, actual)

    def test_simple_nested(self) -> None:
        obj = [
            SimpleDataclass("a", 10, 100.0, None),
            SimpleDataclass("b", 5, 3.14, [])
        ]
        actual = easyjson.dumps(obj, sort_keys=True)
        expected = (
            '[{"a": "a", "b": 10, "c": 100.0, "d": null}, '
            '{"a": "b", "b": 5, "c": 3.14, "d": []}]'
        )
        self.assertEqual(expected, actual)

    def test_complex_1(self) -> None:
        obj = ComplexDataclass(
            a=dict(x="hello", y="world"),
            b=[10, 11, 12],
            c=ComplexDataclass(
                a=dict(x="goodbye", y="world"),
                b=[-100, -200, -300],
                c=None,
            )
        )
        actual = easyjson.dumps(obj, sort_keys=True)
        expected = (
            '{"a": {"x": "hello", "y": "world"}, '
            '"b": [10, 11, 12], '
            '"c": {"a": {"x": "goodbye", "y": "world"}, '
            '"b": [-100, -200, -300], "c": null}}'
        )
        self.assertEqual(expected, actual)

    def test_unserializable_fails(self) -> None:
        obj = UnserializableDataclass(object())
        with self.assertRaises(easyjson.SerializationError):
            easyjson.dumps(obj, sort_keys=True)
