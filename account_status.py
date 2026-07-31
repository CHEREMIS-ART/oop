from enum import Enum, unique
from typing import Union

import errors


@unique
class AccountStatus(Enum):
    ACTIVE = "active"
    FROZEN = "frozen"
    CLOSED = "closed"

    @classmethod
    def from_str(cls, value: Union[str, "AccountStatus"]) -> "AccountStatus":
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            value_lower = value.lower()
            try:
                return AccountStatus(value_lower)
            except ValueError:
                raise errors.InstanceTypeError(
                    cls.__name__, value, (str, AccountStatus), "value"
                )
        raise errors.InstanceTypeError(
            cls.__name__, value, (str, AccountStatus), "value"
        )

    def __str__(self) -> str:
        return self.value.capitalize()
