from typing import Union

from asset import Asset
from stock import Stock
from bond import Bond
from currency import Currency
from asset_type import AssetType
from errors import InstanceTypeError, InvalidOperationError


class Etf(Asset):
    def __init__(
        self,
        symbol: str,
        name: str,
        currency: Union[Currency, str],
        current_price: Union[float, int],
        expense_ratio: float,
        underlying_assets,
    ):
        super().__init__(symbol, name, AssetType.ETF, currency, current_price)
        if not isinstance(expense_ratio, float):
            raise InstanceTypeError(
                self.__class__.__name__, expense_ratio, (float,), "expense_ratio"
            )
        if not (0 <= expense_ratio <= 1):
            raise InvalidOperationError(
                None,
                message="Годовая комиссия фонда в долях должна быть в пределах [0, 1].",
            )
        if not isinstance(underlying_assets, dict):
            raise InstanceTypeError(
                self.__class__.__name__, underlying_assets, (dict,), "underlying_assets"
            )
        if len(underlying_assets) < 1:
            raise InvalidOperationError(
                None, message="Количество активов входящих в ETF должно быть >= 1."
            )
        for symbol, asset_data in underlying_assets.items():
            if not isinstance(symbol, str):
                raise InstanceTypeError(
                    self.__class__.__name__, symbol, (str,), "symbol"
                )
            if not isinstance(asset_data, dict):
                raise InstanceTypeError(
                    self.__class__.__name__,
                    asset_data,
                    (dict,),
                    "underlying_assets[symbol]",
                )
            if "asset" not in asset_data:
                raise InvalidOperationError(
                    None,
                    message="В структуре словаря underlying_assets не найден ключ asset.",
                )
            if "weight" not in asset_data:
                raise InvalidOperationError(
                    None,
                    message="В структуре словаря underlying_assets не найден ключ weight.",
                )
            if len(underlying_assets[symbol]) != 2:
                raise InvalidOperationError(
                    None,
                    message="Нарушена структура вложенного словаря, она должна быть: {'asset': Asset, 'weight': float}.",
                )
            if not isinstance(asset_data["asset"], Asset):
                raise InstanceTypeError(
                    self.__class__.__name__,
                    asset_data["asset"],
                    (Asset,),
                    f"underlying_assets[{symbol}]['asset']",
                )
            if not isinstance(asset_data["weight"], (float, int)):
                raise InstanceTypeError(
                    self.__class__.__name__,
                    asset_data["weight"],
                    (float, int),
                    f"underlying_assets[{symbol}]['weight']",
                )
            if asset_data["weight"] < 0:
                raise InvalidOperationError(
                    None, message="Вес актива не может быть отрицательным."
                )
        self._expense_ratio = expense_ratio
        self._underlying_assets = underlying_assets

    def check_underlying_assets(self) -> bool:
        total_weight = 0.0
        for _, asset_data in self._underlying_assets.items():
            total_weight += asset_data["weight"]
        return abs(total_weight - 1.0) < 1e-8

    def calculate_nav(self) -> float:
        result = 0.0
        for _, asset_data in self._underlying_assets.items():
            result += asset_data["asset"].get_current_price() * asset_data["weight"]
        return result

    def calculate_annual_fee(self, quantity: int) -> float:
        if not isinstance(quantity, int):
            raise InstanceTypeError(
                self.__class__.__name__, quantity, (int,), "quantity"
            )
        if quantity <= 0:
            raise InvalidOperationError(
                None, message="Количество финансовых инструментов должно быть > 0."
            )
        return quantity * self._current_price * self._expense_ratio

    def calculate_annual_income_per_share(self) -> float:
        total_income = 0.0
        for _, asset_data in self._underlying_assets.items():
            if isinstance(asset_data["asset"], Stock):
                total_income += (
                    asset_data["asset"].calculate_dividend_income(1)
                    * asset_data["weight"]
                )
            elif isinstance(asset_data["asset"], Bond):
                total_income += (
                    asset_data["asset"].calculate_annual_coupon() * asset_data["weight"]
                )
        return total_income

    def __str__(self) -> str:
        assets = "Assets:"
        for symbol, asset_data in self._underlying_assets.items():
            assets += f"\n\t- {symbol} - {asset_data['weight']}"
        return (
            super().__str__()
            + f"\n - Годовая комиссия фонда в долях: {self._expense_ratio}"
            f"\n - Список базовых активов: {assets}"
        )
