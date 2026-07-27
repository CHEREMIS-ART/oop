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
        if value is None:
            raise errors.AccountStatusError(
                value, message="Статус аккаунта не может быть None."
            )
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            value_lower = value.lower()
            try:
                return AccountStatus(value_lower)
            except ValueError:
                raise errors.AccountStatusError(value)
        raise errors.AccountStatusError(
            value, message=f"Ожидается str или AccountStatus, получено {type(value)}"
        )

    def __str__(self) -> str:
        return self.value.capitalize()
