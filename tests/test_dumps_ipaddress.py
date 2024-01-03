import unittest
from ipaddress import ip_address, ip_interface, ip_network

import easyjson


class TestDumpsIPAddress(unittest.TestCase):

    def test_ipv4_address(self) -> None:
        obj = ip_address('192.168.0.1')
        actual = easyjson.dumps(obj)
        expected = '"192.168.0.1"'
        self.assertEqual(expected, actual)

    def test_ipv6_address(self) -> None:
        obj = ip_address('2001:db8::')
        actual = easyjson.dumps(obj)
        expected = '"2001:db8::"'
        self.assertEqual(expected, actual)

    def test_ipv4_interface(self) -> None:
        obj = ip_interface('192.168.0.1')
        actual = easyjson.dumps(obj)
        expected = '"192.168.0.1/32"'
        self.assertEqual(expected, actual)

    def test_ipv4_network(self) -> None:
        obj = ip_network('192.168.0.0/28')
        actual = easyjson.dumps(obj)
        expected = '"192.168.0.0/28"'
        self.assertEqual(expected, actual)
