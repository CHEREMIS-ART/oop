from abc import ABC, abstractmethod
from typing import Union

import errors
from account_status import AccountStatus
from owner_info import OwnerInfo


class AbstractAccount(ABC):
    def __init__(
        self, account_id: int, owner_info: OwnerInfo, balance: Union[float, int]
    ) -> None:
        if not isinstance(owner_info, OwnerInfo):
            raise errors.OwnerInfoError(owner_info)
        if owner_info.age < 18:
            raise errors.UnderageError()
        self.__account_id = account_id
        self.account_id_hiden = str(self.__account_id)[-4:]
        self.owner_info = owner_info
        self.balance = balance
        self.status = AccountStatus.ACTIVE

    @property
    def balance(self) -> float:
        return self.__balance

    @balance.setter
    def balance(self, value: Union[float, int]) -> None:
        if not isinstance(value, (float, int)):
            raise errors.InvalidOperationError(
                self.account_id_hiden,
                message=f"Oжидается float или int, передано {type(value)}",
            )
        if value < 0:
            raise errors.InvalidOperationError(
                self.account_id_hiden, message="Баланс не может быть отрицательным"
            )
        self.__balance = value

    def freeze(self) -> None:
        if self.status != AccountStatus.ACTIVE:
            raise errors.AccountFrozenError(
                self.account_id_hiden,
                message=f"Невозможно заморозить счет в статусе {self.status}",
            )
        self.status = AccountStatus.FROZEN
        print(f"Счет ***{self.account_id_hiden} заморожен.")

    def unfreeze(self) -> None:
        if self.status != AccountStatus.FROZEN:
            raise errors.AccountFrozenError(
                self.account_id_hiden,
                message=f"Невозможно разморозить счет в статусе {self.status}",
            )
        self.status = AccountStatus.ACTIVE
        print(f"Счет ***{self.account_id_hiden} разморожен.")

    def close(self) -> None:
        if self.status == AccountStatus.CLOSED:
            raise errors.AccountClosedError(
                self.account_id_hiden,
                message=f"Счет ***{self.account_id_hiden} уже закрыт",
            )
        if self.balance != 0:
            raise errors.BalanceNotZeroError(self.account_id_hiden)
        self.status = AccountStatus.CLOSED
        print(f"Счет ***{self.account_id_hiden} закрыт.")

    @abstractmethod
    def deposit(self, amount: float) -> None:
        pass

    @abstractmethod
    def withdraw(self, amount: float) -> None:
        pass

    @abstractmethod
    def get_account_info(self) -> str:
        pass
