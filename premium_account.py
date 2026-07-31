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
        currency: Union[Currency, str],
        account_id: int = None,
    ):
        super().__init__(owner_info, balance, currency, account_id)
        self._withdrawal_fee = 0.01
        self._daily_deposied_limit = 1_000_000_000
        self._daily_withdrawal_limit = 500_000
        self.__overdraft_limit = -100_000

    def withdraw(self, amount: Union[float, int]) -> None:
        if self._status == AccountStatus.FROZEN:
            raise errors.AccountFrozenError(self._account_id)
        if self._status == AccountStatus.CLOSED:
            raise errors.AccountClosedError(self._account_id)
        if not isinstance(amount, (float, int)):
            raise errors.InstanceTypeError(
                self.__class__.__name__, amount, (float, int), "amount"
            )
        if amount < 0:
            raise errors.InvalidOperationError(
                self._account_id,
                message=f"Счет ***{self._account_id}. Значение должно быть > 0.",
            )
        if amount > self._daily_withdrawal_limit:
            raise errors.InvalidOperationError(
                self._account_id,
                message=f"Счет ***{self._account_id}. Дневной лимит переводов исчерпан.",
            )
        if (self._balance - amount) < self.__overdraft_limit:
            raise errors.InsufficientFundsError(
                self._balance,
                amount,
                message=f"Счет {self._account_id}. Запрошено {amount} {self._currency}, предел овердрафта может быть превышен.",
            )
        bank_interest = amount * self._withdrawal_fee
        total = amount - bank_interest
        self._daily_withdrawal_limit -= amount
        self._balance -= amount
        print(
            f"Счет {self._account_id} снято {total} {self._currency}. Коммисия банка составила: {bank_interest} {self._currency}. Баланс: {self._balance} {self._currency}"
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
            f"\n - Дневной лимит пополнения: {self._daily_deposied_limit} {self._currency}"
            f"\n - Дневной лимит снятия: {self._daily_withdrawal_limit} {self._currency}"
            f"\n - Лимит овердрафта: {self.__overdraft_limit} {self._currency}"
        )
