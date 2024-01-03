import json
import unittest
from collections import UserDict, UserList
from datetime import date, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from ipaddress import ip_address
from pathlib import Path
from uuid import uuid4

from tests.fixtures import SimpleDataclass


class MyDict(UserDict[str, int]):
    pass


class MyList(UserList[int]):
    pass


class TestJSONStdlibFailures(unittest.TestCase):

    def test_userdict_fails(self) -> None:
        obj = MyDict(a=1, b=2)
        with self.assertRaises(TypeError):
            json.dumps(obj)

    def test_userlist_fails(self) -> None:
        obj = MyList()
        obj.append(1)
        with self.assertRaises(TypeError):
            json.dumps(obj)

    def test_dataclass_fails(self) -> None:
        obj = SimpleDataclass("a", 10, 100.0, None)
        with self.assertRaises(TypeError):
            json.dumps(obj)

    def test_date_fails(self) -> None:
        obj = date.today()
        with self.assertRaises(TypeError):
            json.dumps(obj)

    def test_datetime_fails(self) -> None:
        obj = datetime.now()
        with self.assertRaises(TypeError):
            json.dumps(obj)

    def test_timedelta_fails(self) -> None:
        obj = timedelta(days=3)
        with self.assertRaises(TypeError):
            json.dumps(obj)

    def test_uuid_fails(self) -> None:
        obj = uuid4()
        with self.assertRaises(TypeError):
            json.dumps(obj)

    def test_set_fails(self) -> None:
        obj = set([1,2,3])
        with self.assertRaises(TypeError):
            json.dumps(obj)

    def test_frozenset_fails(self) -> None:
        obj = frozenset([1,2,3])
        with self.assertRaises(TypeError):
            json.dumps(obj)

    def test_pathlib_fails(self) -> None:
        obj = Path.home()
        with self.assertRaises(TypeError):
            json.dumps(obj)

    def test_bytes_fails(self) -> None:
        obj = b"a b c d"
        with self.assertRaises(TypeError):
            json.dumps(obj)

    def test_decimal_fails(self) -> None:
        obj = Decimal("0.3")
        with self.assertRaises(TypeError):
            json.dumps(obj)

    def test_complex_fails(self) -> None:
        obj = complex(1, 2)
        with self.assertRaises(TypeError):
            json.dumps(obj)

    def test_fraction_fails(self) -> None:
        obj = Fraction(1, 3)
        with self.assertRaises(TypeError):
            json.dumps(obj)

    def test_ipv4_address_fails(self) -> None:
        obj = ip_address('192.168.0.1')
        with self.assertRaises(TypeError):
            json.dumps(obj)

    def test_ipv6_address_fails(self) -> None:
        obj = ip_address('2001:db8::')
        with self.assertRaises(TypeError):
            json.dumps(obj)

    def test_bare_object_fails(self) -> None:
        with self.assertRaises(TypeError):
            json.dumps(object())
