from typing import Union

from currency import Currency
from asset_type import AssetType
from errors import InstanceTypeError, InvalidOperationError


class Asset:
    def __init__(
        self,
        symbol: str,
        name: str,
        asset_type: str,
        currency: Union[Currency, str],
        current_price: Union[float, int],
    ):
        if not isinstance(symbol, str):
            raise InstanceTypeError(self.__class__.__name__, symbol, (str,), "symbol")
        if not isinstance(name, str):
            raise InstanceTypeError(self.__class__.__name__, name, (str,), "name")
        if not isinstance(current_price, (float, int)):
            raise InstanceTypeError(
                self.__class__.__name__, current_price, (float, int), "current_price"
            )
        if current_price <= 0:
            raise InvalidOperationError(None, message="Цена актива должна быть > 0.")
        self._currency = Currency.from_str(currency)
        self._asset_type = AssetType.from_str(asset_type)
        self._symbol = symbol
        self._name = name
        self._current_price = current_price

    def get_symbol(self) -> str:
        return self._symbol

    def get_current_price(self) -> float:
        return self._current_price

    def update_price(self, new_price: Union[float, int]) -> None:
        if not isinstance(new_price, (float, int)):
            raise InstanceTypeError(
                self.__class__.__name__, new_price, (float, int), "new_price"
            )
        if new_price <= 0:
            raise InvalidOperationError(None, "Цена должна быть > 0")
        self._current_price = new_price

    def __str__(self) -> str:
        return (
            f" - Тикер: {self._symbol}"
            f"\n - Название: {self._name}"
            f"\n - Тип: {self._asset_type}"
            f"\n - Валюта: {self._currency}"
            f"\n - Текущая цена: {self._current_price}"
        )
