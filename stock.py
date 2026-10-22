from typing import Union

from asset import Asset
from asset_type import AssetType
from currency import Currency
from errors import InstanceTypeError, InvalidOperationError
from sectors_type import SectorType


class Stock(Asset):
    def __init__(
        self,
        symbol: str,
        name: str,
        currency: Union[Currency, str],
        current_price: Union[float, int],
        dividend_yield: float,
        sector: SectorType,
    ):
        super().__init__(symbol, name, AssetType.STOCK, currency, current_price)
        if not isinstance(dividend_yield, float):
            raise InstanceTypeError(
                self.__class__.__name__, dividend_yield, (float,), "dividend_yield"
            )
        if not (0 <= dividend_yield <= 1):
            raise InvalidOperationError(
                None,
                message=f"Дивидендная доходность должна быть в пределах [0, 1].",
            )
        self._sector = SectorType.from_str(sector)
        self._dividend_yield = dividend_yield

    def calculate_dividend_income(self, quantity: int,) -> float:
        if not isinstance(quantity, int):
            raise InstanceTypeError(
                self.__class__.__name__, quantity, (int,), "quantity"
            )
        if quantity <= 0:
            raise InvalidOperationError(
                None, message="Количество финансовых инструментов должно быть > 0."
            )

        return quantity * self._current_price * self._dividend_yield

    def __str__(self) -> str:
        return (
            super().__str__() + f"\n - Дивидендная доходность: {self._dividend_yield}"
            f"\n - Сектор экономики: {self._sector}"
        )
