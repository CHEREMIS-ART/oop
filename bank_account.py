from uuid import uuid4
from typing import Union

from abstract_account import AbstractAccount
from owner_info import OwnerInfo
from currency import Currency
from account_status import AccountStatus
import errors


class BankAccount(AbstractAccount):
    def __init__(
        self,
        owner_info: OwnerInfo,
        balance: Union[float, int],
        currency: Union[Currency, str],
        account_id=None,
    ):
        if account_id is None:
            account_id = int(str(uuid4().int)[:16])
        super().__init__(account_id, owner_info, balance)
        self._currency = Currency.from_str(currency)
        self._withdrawal_fee = 0.015
        self._daily_deposied_limit = 250_000
        self._daily_withdrawal_limit = 100_000

    def deposit(self, amount: Union[float, int]) -> None:
        if self._status == AccountStatus.FROZEN:
            raise errors.AccountFrozenError(self._account_id)
        if self._status == AccountStatus.CLOSED:
            raise errors.AccountClosedError(self._account_id)
        if not isinstance(amount, (float, int)):
            raise errors.InvalidOperationError(
                self._account_id,
                message=f"Oжидается float или int, передано {type(amount)}",
            )
        if amount < 0:
            raise errors.InvalidOperationError(
                self._account_id,
                message="Пополнить счет можно только положительным значением",
            )
        self._balance += amount
        print(
            f"Счет {self._account_id} пополнился на {amount} {self._currency}. Баланс: {self._balance} {self._currency}"
        )

    def withdraw(self, amount: Union[float, int]) -> None:
        if self._status == AccountStatus.FROZEN:
            raise errors.AccountFrozenError(self._account_id)
        if self._status == AccountStatus.CLOSED:
            raise errors.AccountClosedError(self._account_id)
        if not isinstance(amount, (float, int)):
            raise errors.InvalidOperationError(
                self._account_id,
                message=f"Oжидается float или int, передано {type(amount)}",
            )
        if amount < 0:
            raise errors.InvalidOperationError(
                self._account_id,
                message=f"Счет {self._account_id}. Значение amount должно быть > 0.",
            )
        if amount > self._balance:
            raise errors.InsufficientFundsError(self._balance, amount)
        self._balance -= amount
        print(
            f"Счет {self._account_id} снято {amount} {self._currency}. Баланс: {self._balance} {self._currency}"
        )

    def reset_daily_limits(self) -> None:
        self._daily_deposied_limit = 250_000
        self._daily_withdrawal_limit = 100_000

    def get_account_info(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return (
            f" - Тип: {self.__class__.__name__}"
            f"\n - Клиент: {self._owner_info}"
            f"\n - Счет: {self._account_id}"
            f"\n - Статус: {self._status}"
            f"\n - Баланс: {self._balance}"
            f"\n - Валюта: {self._currency}"
        )
