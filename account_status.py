from enum import Enum, auto


class AccountStatus(Enum):
    ACTIVE = auto()
    FROZEN = auto()
    CLOSED = auto()

    def __str__(self) -> str:
        return self.name.capitalize()
