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
        self.__min_balance = self.balance
        self.monthly_interest = monthly_interest

    @property
    def monthly_interest(self) -> Union[float, int]:
        return self.__monthly_interest

    @monthly_interest.setter
    def monthly_interest(self, value: Union[float, int]) -> None:
        if not isinstance(value, (float, int)):
            raise errors.InvalidOperationError(
                self.account_id_hiden,
                message=f"Ожидается float или int, принято {type(value)}",
            )
        interest = Currency.get_interest_by_currency(self.currency)
        if not (value > 0 and value <= interest):
            raise errors.InvalidOperationError(
                self.account_id_hiden,
                message=f"Месечная ставка для валюты {self.currency} должна быть от 0 до {interest}",
            )
        self.__monthly_interest = value

    def apply_monthly_interest(self) -> None:
        if self.status == AccountStatus.FROZEN:
            raise errors.AccountFrozenError(
                self.account_id_hiden,
                f"Счет ***{self.account_id_hiden} заморожен. Операция недоступна.",
            )
        if self.status == AccountStatus.CLOSED:
            raise errors.AccountClosedError(
                self.account_id_hiden,
                f"Счет ***{self.account_id_hiden} закрыт. Операция недоступна.",
            )
        monthly_interest = self.__min_balance * (self.monthly_interest / 100)
        self.balance += monthly_interest
        self.__min_balance = self.balance
        print(
            f"Счет ***{self.account_id_hiden}. Начислена месечная доходность: {monthly_interest} {self.currency}"
        )

    def withdraw(self, amount: Union[float, int]) -> None:
        super().withdraw(amount)
        if self.balance < self.__min_balance:
            self.__min_balance = self.balance

    def get_account_info(self) -> str:
        return str(self)

    def __str__(self) -> str:
        parent_str = super().__str__()
        return parent_str + f"\n - Месячная ставка доходности: {self.monthly_interest} %"
