from enum import Enum, unique
from typing import Union

from errors import InstanceTypeError


class ClientStatus(Enum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"
    PENDING_VERIFICATION = "PENDING VERIFICATION"
    RESTRICTED = "RESTRICTED"

    def from_str(cls, value: Union[str, "ClientStatus"]) -> "ClientStatus":
        if isinstance(value, "ClientStatus"):
            return value
        if isinstance(value, str):
            value_upper = value.upper()
            try:
                return ClientStatus(value_upper)
            except ValueError:
                raise InstanceTypeError(
                    cls.__name__, value, (str, ClientStatus), "value"
                )
        raise InstanceTypeError(cls.__name__, value, (str, ClientStatus), "value")

    def __str__(self) -> str:
        return self.value
