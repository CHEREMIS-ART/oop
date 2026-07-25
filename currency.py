from enum import Enum, auto


class Currency(Enum):
    RUB = auto()
    USD = auto()
    EUR = auto()
    KZT = auto()
    CNY = auto()

    def __str__(self) -> str:
        return self.name.upper()
