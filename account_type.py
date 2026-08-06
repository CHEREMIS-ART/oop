from enum import Enum, unique
from typing import Union

from errors import InstanceTypeError


class AccountType(Enum):
    INVESTMENT = "INVESTMENT"
    PREMIUM = "PREMIUM"
    SAVINGS = "SAVINGS"

    @classmethod
    def from_str(cls, value: Union[str, "AccountType"]) -> "AccountType":
        if isinstance(value, "AccountType"):
            return value
        if isinstance(value, str):
            value_upper = value.upper()
            try:
                return AccountType(value_upper)
            except ValueError:
                raise InstanceTypeError(
                    cls.__name__, value, (str, AccountType), "value"
                )
        raise InstanceTypeError(cls.__name__, value, (str, AccountType), "value")

    def __str__(self) -> str:
        return self.value
