from typing import Union

from bank_account import BankAccount
from owner_info import OwnerInfo
from currency import Currency
from account_status import AccountStatus
import errors


class PremiumAccount(BankAccount):
    def __init__(
        self,
        owner_info: OwnerInfo,
        balance: Union[float, int],
        currency: Currency,
        account_id: int = None,
    ):
        self.__overdraft_limit = -100_000
        super().__init__(owner_info, balance, currency, account_id)
        self._withdrawal_fee = 0.01
        self._daily_deposied_limit = 1_000_000_000
        self._daily_withdrawal_limit = 500_000

    @property
    def balance(self) -> Union[float, int]:
        return self._balance

    @balance.setter
    def balance(self, value: Union[float, int]) -> None:
        if self.status == AccountStatus.FROZEN:
            raise errors.AccountFrozenError(self.account_id_hiden)
        if self.status == AccountStatus.CLOSED:
            raise errors.AccountClosedError(self.account_id_hiden)
        if not isinstance(value, (float, int)):
            raise errors.InvalidOperationError(
                self.account_id_hiden,
                message=f"Oжидается float или int, передано {type(amount)}",
            )
        if value < self.__overdraft_limit:
            raise errors.InsufficientFundsError(
                self.__overdraft_limit,
                value,
                message=f"Счет ***{self.account_id_hiden}. Запрошено {value} {self.currency}, предел овердрафта может быть превышен.",
            )
        self._balance = value

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
        if amount < 0:
            raise errors.InvalidOperationError(
                self.account_id_hiden,
                message=f"Счет ***{self.account_id_hiden}. Значение должно быть > 0.",
            )
        if amount > self._daily_withdrawal_limit:
            raise errors.InvalidOperationError(
                self.account_id_hiden,
                message=f"Счет ***{self.account_id_hiden}. Дневной лимит переводов исчерпан.",
            )
        if (self.balance - amount) < self.__overdraft_limit:
            raise errors.InsufficientFundsError(
                self.balance,
                amount,
                message=f"Счет ***{self.account_id_hiden}. Запрошено {amount} {self.currency}, предел овердрафта может быть превышен.",
            )
        bank_interest = amount * (self._withdrawal_fee / 100)
        total = amount - bank_interest
        self._daily_withdrawal_limit -= amount
        self.balance -= amount
        print(
            f"Счет ***{self.account_id_hiden} снято {total} {self.currency}. Коммисия банка составила: {bank_interest} {self.currency}. Баланс: {self.balance} {self.currency}"
        )

    def reset_daily_limits(self) -> None:
        self._daily_deposied_limit = 1_000_000_000
        self._daily_withdrawal_limit = 500_000

    def get_account_info(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return (
            super().__str__()
            + f"\n - Комиссия на операцию перевода: {self._withdrawal_fee} %"
            f"\n - Дневной лимит пополнения: {self._daily_deposied_limit} {self.currency}"
            f"\n - Дневной лимит снятия: {self._daily_withdrawal_limit} {self.currency}"
            f"\n - Лимит овердрафта: {self.__overdraft_limit} {self.currency}"
        )
