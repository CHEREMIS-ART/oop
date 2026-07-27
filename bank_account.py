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
        balance: float,
        currency: Union[Currency, str],
        account_id=None,
    ):
        if account_id is None:
            account_id = uuid4().int
        super().__init__(account_id, owner_info, balance)
        self.currency = Currency.from_str(currency)

    def deposit(self, amount: Union[float, int]) -> None:
        if self.status == AccountStatus.FROZEN:
            raise errors.AccountFrozenError(self.account_id_hiden)
        if self.status == AccountStatus.CLOSED:
            raise errors.AccountClosedError(self.account_id_hiden)
        if not isinstance(amount, (float, int)):
            raise errors.InvalidOperationError(
                self.account_id_hiden,
                message=f"Oжидается float или int, передано {type(amount)}",
            )
        if amount <= 0:
            raise errors.InvalidOperationError(
                self.account_id_hiden,
                message="Пополнить счет можно только положительным значением",
            )
        self.balance += amount
        print(
            f"Счет ***{self.account_id_hiden} пополнился на {amount} {self.currency}. Баланс: {self.balance} {self.currency}"
        )

    def withdraw(self, amount: Union[float, int]) -> None:
        if self.status == AccountStatus.FROZEN:
            raise errors.AccountFrozenError(self.account_id_hiden)
        if self.status == AccountStatus.CLOSED:
            raise errors.AccountClosedError(self.account_id_hiden)
        if not isinstance(amount, (float, int)):
            raise errors.InvalidOperationError(
                self.account_id_hiden,
                message=f"Oжидается float или int, передано {type(amount)}",
            )
        if amount <= 0:
            raise errors.InvalidOperationError(
                self.account_id_hiden,
                message=f"Счет ***{self.account_id_hiden}. Значение amount должно быть > 0.",
            )
        if amount > self.balance:
            raise errors.InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        print(
            f"Счет ***{self.account_id_hiden} снято {amount} {self.currency}. Баланс: {self.balance} {self.currency}"
        )

    def get_account_info(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return (
            f" - Тип: {self.__class__.__name__}"
            f"\n - Клиент: {self.owner_info}"
            f"\n - Счет: ***{self.account_id_hiden}"
            f"\n - Статус: {self.status}"
            f"\n - Баланс: {self.balance}"
            f"\n - Валюта: {self.currency}"
        )
