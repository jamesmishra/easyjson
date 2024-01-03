import dataclasses
import datetime
from typing import Any, Dict, List, Optional


@dataclasses.dataclass
class SimpleDataclass:
    a: str
    b: int
    c: float
    d: Any


@dataclasses.dataclass
class ComplexDataclass:
    a: Dict[str, str]
    b: List[int]
    c: Optional["ComplexDataclass"]


@dataclasses.dataclass
class UnserializableDataclass:
    a: Any


dt_stamp = datetime.datetime(
    year=2023,
    month=10,
    day=15,
    hour=3,
    minute=10,
    second=30,
    microsecond=1234,
)