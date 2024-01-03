import unittest
import uuid

import easyjson


class TestDumpsUUID(unittest.TestCase):
    def test_hardcoded_uuid(self) -> None:
        obj = uuid.UUID('dbe95ebe-dcd9-4774-8f69-07e8d619e16b')
        actual = easyjson.dumps(obj)
        expected = '"dbe95ebe-dcd9-4774-8f69-07e8d619e16b"'
        self.assertEqual(expected, actual)

    def test_varying_uuid(self) -> None:
        obj = uuid.uuid4()
        actual = easyjson.dumps(obj)
        expected = f'"{obj}"'
        self.assertEqual(expected, actual)
