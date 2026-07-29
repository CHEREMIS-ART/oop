from typing import Union

from bank_account import BankAccount
from owner_info import OwnerInfo
from currency import Currency
from account_status import AccountStatus
import errors


class SavingsAccount(BankAccount):

    def __init__(
        self,
        owner_info: OwnerInfo,
        balance: Union[float, int],
        currency: Union[Currency, str],
        account_id: int = None,
        monthly_interest: Union[float, int] = 0.01,
    ):
        super().__init__(owner_info, balance, currency, account_id)
        if not isinstance(monthly_interest, (float, int)):
            raise errors.InvalidOperationError(
                self._account_id,
                message=f"Ожидается для monthly_interest тип: float или int, принят тип: {type(value)}",
            )
        interest = Currency.get_interest_by_currency(self._currency)
        if not (monthly_interest > 0 and monthly_interest <= interest):
            raise errors.InvalidOperationError(
                self._account_id,
                message=f"Месечная ставка для валюты {self._currency} должна быть от 0 до {interest}",
            )
        self.__min_balance = self._balance
        self.__monthly_interest = monthly_interest

    def apply_monthly_interest(self) -> None:
        if self._status == AccountStatus.FROZEN:
            raise errors.AccountFrozenError(
                self._account_id,
                f"Счет {self._account_id} заморожен. Операция недоступна.",
            )
        if self.status == AccountStatus.CLOSED:
            raise errors.AccountClosedError(
                self._account_id,
                f"Счет {self._account_id} закрыт. Операция недоступна.",
            )
        monthly_interest = self.__min_balance * (self.__monthly_interest / 100)
        self._balance += monthly_interest
        self.__min_balance = self._balance
        print(
            f"Счет {self._account_id}. Начислена месечная доходность: {monthly_interest} {self._currency}"
        )

    def withdraw(self, amount: Union[float, int]) -> None:
        super().withdraw(amount)
        if self._balance < self.__min_balance:
            self.__min_balance = self._balance

    def get_account_info(self) -> str:
        return str(self)

    def __str__(self) -> str:
        parent_str = super().__str__()
        return (
            parent_str + f"\n - Месячная ставка доходности: {self.__monthly_interest} %"
        )
