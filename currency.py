from enum import Enum, unique
from typing import Union

import errors


@unique
class Currency(Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
    KZT = "KZT"
    CNY = "CNY"

    @classmethod
    def from_str(cls, value: Union[str, "Currency"]) -> "Currency":
        if value is None:
            raise errors.CurrencyError(value, message=f"Валюта не может быть None.")
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            value_upper = value.upper()
            try:
                return Currency(value_upper)
            except ValueError:
                raise errors.CurrencyError(value)
        raise errors.CurrencyError(
            value, message=f"Ожидается str или Currency, получено {type(value)}"
        )

    @classmethod
    def get_interest_by_currency(
        cls, currency: Union[str, "Currency"]
    ) -> Union[float, int]:
        if currency is Currency.RUB:
            return 1.17
        if currency is Currency.USD:
            return 0.30
        if currency is Currency.EUR:
            return 0.19
        if currency is Currency.KZT:
            return 1.40
        if currency is Currency.CNY:
            return 0.25

    def __str__(self) -> str:
        return self.value
