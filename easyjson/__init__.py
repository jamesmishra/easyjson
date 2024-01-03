from __future__ import annotations

import argparse
import dataclasses
import json
from base64 import standard_b64encode
from collections.abc import Mapping, Sequence, Set
from datetime import date, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
from pathlib import Path
from types import NoneType
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union, cast
from uuid import UUID

ONE_DAY_IN_SECONDS: int = 86400


ONE_HOUR_IN_SECONDS: int = 3600


ONE_MINUTE_IN_SECONDS: int = 60


JSON_PRIMITIVE_TYPE = Union[None, bool, str, int, float]


JSON_TYPE = Union[JSON_PRIMITIVE_TYPE, Dict[str, "JSON_TYPE"], List["JSON_TYPE"]]


DEFAULT_BASE64_PREFIX = "base64: "


DEFAULT_TIMEDELTA_PREFIX = "Duration: "


class SerializationError(TypeError):
    def __init__(self, obj: Any):
        obj_type = type(obj).__name__
        msg = f"Object of type `{obj_type}` is not JSON serializable."
        super().__init__(msg)


def obj_public_attrs(obj: Any) -> Dict[str, Any]:
    """
    This is similar to `vars()` but it also returns properties
    from an object's class.
    """
    out: Dict[str, Any] = {}
    for name in dir(obj):
        if name.startswith("_"):
            continue
        value = getattr(obj, name)
        if callable(value):
            continue
        out[name] = value
    return out


class Encoder:
    types_to_str = (
        UUID,
        Path,
        IPv4Address,
        IPv6Address,
        IPv4Interface,
        IPv6Interface,
        IPv4Network,
        IPv6Network,
    )

    types_to_isoformat = (date, datetime)

    #types_via_sequence = (list, tuple, set, frozenset)

    #types_via_mapping = (dict,)

    def __init__(
        self,
        decimal_as: Optional[str] = "str",
        fraction_as: Optional[str] = "str",
        bytes_as: Optional[str] = "base64",
        use_dir: bool = False,
        base64_prefix: str = DEFAULT_BASE64_PREFIX,
        timedelta_prefix: str = DEFAULT_TIMEDELTA_PREFIX,
    ) -> None:
        self.decimal_as = decimal_as
        self.fraction_as = fraction_as
        self.bytes_as = bytes_as
        self.use_dir = use_dir
        self.base64_prefix = base64_prefix
        self.timedelta_prefix = timedelta_prefix

        class JSONEncoder(json.JSONEncoder):
            def default(inner_self, obj: Any) -> JSON_TYPE:
                return self.obj_to_bare(obj, recursive=False)
        self._Encoder = JSONEncoder

    def _encode_bytes(self, obj: bytes) -> str:
        if self.bytes_as == "base64":
            return standard_b64encode(obj).decode("utf-8")
        if self.bytes_as is None:
            raise SerializationError(obj)
        try:
            return obj.decode(self.bytes_as)
        except LookupError as exc:
            raise SerializationError(obj) from exc

    def _timedelta_to_str(self, td: timedelta) -> str:
        total_seconds: int = int(td.total_seconds())
        if total_seconds == 0:
            return self.timedelta_prefix + "0 microseconds"
        days: int = total_seconds // ONE_DAY_IN_SECONDS
        days_rem_in_seconds: int = total_seconds % ONE_DAY_IN_SECONDS
        hours: int = days_rem_in_seconds // ONE_HOUR_IN_SECONDS
        hours_rem_in_seconds: int = days_rem_in_seconds % ONE_HOUR_IN_SECONDS
        minutes: int = hours_rem_in_seconds // ONE_MINUTE_IN_SECONDS
        seconds: int = hours_rem_in_seconds % ONE_MINUTE_IN_SECONDS
        out: List[str] = []
        if days:
            out.append(f"{days} days")
        if hours:
            out.append(f"{hours} hours")
        if minutes:
            out.append(f"{minutes} minutes")
        if seconds:
            out.append(f"{seconds} seconds")
        if td.microseconds:
            out.append(f"{td.microseconds} microseconds")
        out_str = ", ".join(out)
        if self.timedelta_prefix:
            return self.timedelta_prefix + out_str
        return out_str

    def _complex_to_str(self, obj: complex) -> str:
        return str(obj)[1:-1]

    def _decimal_to_str(self, obj: Decimal) -> Union[str, float, int]:
        # TODO(jamesmishra): Turn string types into enums.
        if self.decimal_as == "str":
            return str(obj)
        if self.decimal_as == "float":
            return float(obj)
        if self.decimal_as == "int":
            return int(obj)
        # TODO(jamesmishra): Create a custom exception class for this branch.
        if self.decimal_as is None:
            raise SerializationError(obj)
        raise RuntimeError("Unknown decimal_as value.")

    def _fraction_to_str(self, obj: Fraction) -> Union[str, float, int]:
        if self.fraction_as == "str":
            return str(obj)
        if self.fraction_as == "float":
            return float(obj)
        if self.fraction_as == "int":
            return int(obj)
        # TODO(jamesmishra): Create a custom exception class for this branch.
        if self.fraction_as is None:
            raise SerializationError(obj)
        raise RuntimeError("Unknown fraction_as value.")

    def obj_to_bare(self, obj: Any, *, recursive: bool = False) -> JSON_TYPE:
        # TODO(jamesmishra): Check the performance implications of the next line.
        if isinstance(obj, (bool, str, int, float, NoneType)):
            return cast(Union[bool, str, int, float, None], obj)
        if isinstance(obj, bytes):
            return self._encode_bytes(obj)
        if isinstance(obj, self.types_to_str):
            return str(obj)
        if isinstance(obj, self.types_to_isoformat):
            return obj.isoformat()
        if isinstance(obj, timedelta):
            return self._timedelta_to_str(obj)
        if isinstance(obj, complex):
            return self._complex_to_str(obj)
        if isinstance(obj, Decimal):
            return self._decimal_to_str(obj)
        if isinstance(obj, Fraction):
            return self._fraction_to_str(obj)

        # Converting list types
        if isinstance(obj, (Sequence, Set)):
            if recursive:
                return [
                    self.obj_to_bare(item, recursive=True)
                    for item in obj
                ]
            return list(obj)

        # Converting dictionary types
        if isinstance(obj, Mapping):
            if recursive:
                return {
                    key: self.obj_to_bare(obj[key], recursive=True)
                    for key in obj
                }
            return dict(obj)
        mapping: Optional[Dict[str, Any]] = None
        if dataclasses.is_dataclass(obj):
            mapping = dataclasses.asdict(obj)
        elif isinstance(obj, argparse.Namespace):
            mapping = vars(obj)
        elif self.use_dir:
            mapping = obj_public_attrs(obj)
        if mapping is not None:
            if recursive:
                return {
                    key: self.obj_to_bare(mapping[key], recursive=True)
                    for key in mapping
                }
            return mapping

        # Now calling to_bare() on the object to see what happens.
        try:
            mapping = obj.to_bare()
        except AttributeError:
            pass

        # Could not convert the object we found.
        raise SerializationError(obj)

    @property
    def Class(self) -> Type[json.JSONEncoder]:
        return self._Encoder

    def dumps(
        self,
        obj: Any,
        *,
        skipkeys: bool=False,
        ensure_ascii: bool=True,
        check_circular: bool=True,
        allow_nan: bool=True,
        indent: Optional[int]=None,
        separators: Optional[Tuple[str, str]]=None,
        default: Optional[Callable[[Any], JSON_TYPE]]=None,
        sort_keys: bool=False,
    ) -> str:
        return json.dumps(
            obj=obj,
            cls=self._Encoder,
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            indent=indent,
            separators=separators,
            default=default,
            sort_keys=sort_keys,
        )

    def to_bare(self) -> Dict[str, Union[str, bool, None]]:
        return dict(
            decimal_as=self.decimal_as,
            fraction_as=self.fraction_as,
            bytes_as=self.bytes_as,
            use_dir=self.use_dir,
            base64_prefix=self.base64_prefix,
            timedelta_prefix=self.timedelta_prefix,
        )

default_encoder = Encoder()


def dumps(
    obj: Any,
    *,
    skipkeys: bool=False,
    ensure_ascii: bool=True,
    check_circular: bool=True,
    allow_nan: bool=True,
    indent: Optional[int]=None,
    separators: Optional[Tuple[str, str]]=None,
    default: Optional[Callable[..., Any]]=None,
    sort_keys: bool=False,
) -> str:
    return json.dumps(
        obj=obj,
        cls=default_encoder.Class,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        indent=indent,
        separators=separators,
        default=default,
        sort_keys=sort_keys,
    )
