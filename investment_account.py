from typing import Union

from bank_account import BankAccount
from owner_info import OwnerInfo
from currency import Currency
from asset import Asset
from account_status import AccountStatus
from stock import Stock
from bond import Bond
from etf import Etf
import errors


class InvestmentAccount(BankAccount):
    def __init__(
        self,
        owner_info: OwnerInfo,
        balance: Union[float, int],
        currency: Union[Currency, str],
        account_id: int = None,
    ):
        super().__init__(owner_info, balance, currency, account_id)
        self._assets = {}  # {symbol: {"asset": Asset, "quantity": int}}

    def withdraw(self, amount: Union[float, int]) -> None:
        super().withdraw(amount)

    def buy_asset(self, asset: Asset, quantity: int) -> None:
        if self._status == AccountStatus.FROZEN:
            raise errors.AccountFrozenError(self._account_id)
        if self._status == AccountStatus.CLOSED:
            raise errors.AccountClosedError(self._account_id)
        if not isinstance(quantity, int):
            raise errors.InstanceTypeError(
                self.__class__.__name__, quantity, (int,), "quantity"
            )
        if quantity <= 0:
            raise errors.InvalidOperationError(
                None, message="Количество финансовых инструментов должно быть > 0."
            )
        if not isinstance(asset, Asset):
            raise errors.InstanceTypeError(
                self.__class__.__name__, asset, (Asset,), "asset"
            )
        total_cost = quantity * asset.get_current_price()
        if total_cost > self._balance:
            raise errors.InsufficientFundsError(self._balance, total_cost)
        self._balance -= total_cost

        symbol = asset.get_symbol()
        if symbol in self._assets:
            self._assets[symbol]["quantity"] += quantity
        else:
            self._assets[symbol] = {"asset": asset, "quantity": quantity}

        print(
            f"Счет {self._account_id}. Куплено {quantity} {symbol} на сумму {total_cost} {self._currency}. Остаток: {self._balance} {self._currency}"
        )

    def sell_asset(self, symbol: str, quantity: int) -> None:
        if self._status == AccountStatus.FROZEN:
            raise errors.AccountFrozenError(self._account_id)
        if self._status == AccountStatus.CLOSED:
            raise errors.AccountClosedError(self._account_id)
        if not isinstance(quantity, int):
            raise errors.InstanceTypeError(
                self.__class__.__name__, quantity, (int,), "quantity"
            )
        if quantity <= 0:
            raise errors.InvalidOperationError(
                None, message="Количество финансовых инструментов должно быть > 0."
            )
        if not isinstance(symbol, str):
            raise errors.InstanceTypeError(
                self.__class__.__name__, symbol, (str,), "symbol"
            )

        if symbol not in self._assets:
            raise errors.InvalidOperationError(
                self._account_id, f"Актив {symbol} не найден в портфеле."
            )
        if self._assets[symbol]["quantity"] < quantity:
            raise errors.InvalidOperationError(
                self._account_id,
                message=f"Счет {self._account_id}. Недостаточно {symbol} для продажи.",
            )

        asset = self._assets[symbol]["asset"]
        total_revenue = quantity * asset.get_current_price()
        self._balance += total_revenue

        self._assets[symbol]["quantity"] -= quantity
        if self._assets[symbol]["quantity"] == 0:
            del self._assets[symbol]

        print(
            f"Счет {self._account_id}. Продано {quantity} {symbol} на сумму {total_revenue} {self._currency}. Остаток: {self._balance} {self._currency}"
        )

    def get_total_asset_value(self) -> float:
        total = 0.0
        for data in self._assets.values():
            total += data["quantity"] * data["asset"].get_current_price()
        return total

    def project_yearly_growth(
        self, years: int, price_growth_rate: float = 0.05
    ) -> float:
        if self._status == AccountStatus.FROZEN:
            raise errors.AccountFrozenError(self._account_id)
        if self._status == AccountStatus.CLOSED:
            raise errors.AccountClosedError(self._account_id)
        if not isinstance(years, int):
            raise errors.InstanceTypeError(
                self.__class__.__name__, years, (int,), "years"
            )
        if years < 0:
            raise errors.InvalidOperationError(
                self._account_id, "Количество лет должно быть >= 0"
            )
        if not isinstance(price_growth_rate, (float, int)):
            raise errors.InstanceTypeError(
                self.__class__.__name__,
                price_growth_rate,
                (float, int),
                "price_growth_rate",
            )

        asset_value = self.get_total_asset_value()
        balance = self._balance

        annual_income = 0.0
        for data in self._assets.values():
            asset = data["asset"]
            quantity = data["quantity"]
            if isinstance(asset, Stock):
                annual_income += asset.calculate_dividend_income(quantity)
            elif isinstance(asset, Bond):
                annual_income += asset.calculate_annual_coupon() * quantity
            elif isinstance(asset, Etf):
                annual_income += asset.calculate_annual_income_per_share() * quantity

        total_value = balance + asset_value
        if total_value == 0:
            return 0.0

        total_return = (price_growth_rate * asset_value + annual_income) / total_value
        future_value = total_value * (1 + total_return) ** years

        return future_value

    def accrue_income(self, days: int = 365) -> None:
        if self._status == AccountStatus.FROZEN:
            raise errors.AccountFrozenError(self._account_id)
        if self._status == AccountStatus.CLOSED:
            raise errors.AccountClosedError(self._account_id)
        if not isinstance(days, int):
            raise errors.InstanceTypeError(
                self.__class__.__name__, days, (int,), "days"
            )
        if days <= 0:
            raise errors.InvalidOperationError(
                self._account_id,
                message=f"Счет {self._account_id}. Количество дней для расчета дохода по активам должно быть > 0.",
            )

        total_income = 0.0
        for symbol, asset_data in self._assets.items():
            asset = asset_data["asset"]
            quantity = asset_data["quantity"]

            if isinstance(asset, Stock):
                annual_income = asset.calculate_dividend_income(quantity)
            elif isinstance(asset, Bond):
                annual_income = asset.calculate_annual_coupon() * quantity
            elif isinstance(asset, Etf):
                annual_income = asset.calculate_annual_income_per_share() * quantity

            total_income += annual_income * (days / 365.25)

        self._balance += total_income
        print(
            f"Счёт {self._account_id}. Начислен доход за {days} дней: "
            f"{total_income} {self._currency}. Баланс: {self._balance} {self._currency}"
        )

    def get_account_info(self):
        return str(self)

    def __str__(self) -> str:
        lines = [super().__str__()]
        lines.append(" - Портфель:")

        if not self._assets:
            lines.append("   (пуст)")
        else:
            total_asset_value = 0.0
            for symbol, data in self._assets.items():
                asset = data["asset"]
                quantity = data["quantity"]
                price = asset.get_current_price()
                value = quantity * price
                total_asset_value += value
                lines.append(
                    f"   {symbol}: {quantity} шт. × {price} = {value} {self._currency}"
                )

            lines.append(f" - Стоимость активов: {total_asset_value} {self._currency}")
            lines.append(f" - Денежный остаток: {self._balance} {self._currency}")
            lines.append(
                f" - Общая стоимость портфеля: {self._balance + total_asset_value} {self._currency}"
            )

        return "\n".join(lines)
