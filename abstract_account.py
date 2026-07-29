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
        if not isinstance(account_id, int):
            raise errors.InvalidOperationError(
                None, message=f"Oжидается для id тип: int, передан тип: {type(amount)}"
            )
        if not isinstance(balance, (float, int)):
            raise errors.InvalidOperationError(
                account_id,
                message=f"Oжидается для balance тип: int или float, передан тип: {type(amount)}",
            )
        if balance < 0:
            raise errors.InvalidOperationError(
                account_id, message=f"Баланс должен быть положительным."
            )
        self._account_id = account_id
        self._owner_info = owner_info
        self._balance = balance
        self._status = AccountStatus.ACTIVE

    def freeze(self) -> None:
        if self._status != AccountStatus.ACTIVE:
            raise errors.AccountFrozenError(
                self._account_id,
                message=f"Невозможно заморозить счет в статусе {self._status}",
            )
        self._status = AccountStatus.FROZEN
        print(f"Счет {self._account_id} заморожен.")

    def unfreeze(self) -> None:
        if self._status != AccountStatus.FROZEN:
            raise errors.AccountFrozenError(
                self._account_id,
                message=f"Невозможно разморозить счет в статусе {self._status}",
            )
        self._status = AccountStatus.ACTIVE
        print(f"Счет {self._account_id} разморожен.")

    def close(self) -> None:
        if self._status == AccountStatus.CLOSED:
            raise errors.AccountClosedError(
                self._account_id,
                message=f"Счет ***{self._account_id} уже закрыт",
            )
        if self._balance != 0:
            raise errors.BalanceNotZeroError(self._account_id)
        self._status = AccountStatus.CLOSED
        print(f"Счет {self._account_id} закрыт.")

    @abstractmethod
    def deposit(self, amount: float) -> None:
        pass

    @abstractmethod
    def withdraw(self, amount: float) -> None:
        pass

    @abstractmethod
    def get_account_info(self) -> str:
        pass
