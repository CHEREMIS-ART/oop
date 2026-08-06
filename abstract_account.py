from abc import ABC, abstractmethod
from typing import Union

import errors
from account_status import AccountStatus
from client import Client
from client_status import ClientStatus


class AbstractAccount(ABC):
    def __init__(
        self, account_id: int, client: Client, balance: Union[float, int]
    ) -> None:
        if not isinstance(client, Client):
            raise errors.InstanceTypeError(
                self.__class__.__name__, client, (Client,), "client"
            )
        if not isinstance(account_id, int):
            raise errors.InstanceTypeError(
                self.__class__.__name__, account_id, (int,), "account_id"
            )
        if not isinstance(balance, (float, int)):
            raise errors.InstanceTypeError(
                self.__class__.__name__, balance, (float, int), "balance"
            )
        if balance < 0:
            raise errors.InvalidOperationError(
                account_id, message=f"Баланс должен быть положительным."
            )
        self._account_id = account_id
        self._client = client
        self._balance = balance
        self._status = AccountStatus.ACTIVE

    def get_account_id(self) -> int:
        return self._account_id

    def get_account_client(self) -> Client:
        return self._client

    def _ensure_client_status(self, allowed_statuses: tuple) -> None:
        client_status = self._client.get_status()
        if client_status == ClientStatus.FROZEN:
            raise errors.ClientFrozenError()
        if client_status == ClientStatus.CLOSED:
            raise errors.ClientClosedError()
        if client_status == ClientStatus.PENDING_VERIFICATION:
            raise errors.ClientNotVerifiedError()
        if client_status not in allowed_statuses:
            raise errors.ClientStatusTypeError(
                f"Статус клиента {client_status} не разрешён для данной операции."
            )

    def freeze(self) -> None:
        self._ensure_client_status((ClientStatus.ACTIVE,))
        if self._status != AccountStatus.ACTIVE:
            raise errors.AccountFrozenError(
                self._account_id,
                message=f"Невозможно заморозить счет в статусе {self._status}",
            )
        self._status = AccountStatus.FROZEN
        print(f"Счет {self._account_id} заморожен.")

    def unfreeze(self) -> None:
        self._ensure_client_status((ClientStatus.ACTIVE, ClientStatus.RESTRICTED))
        if self._status != AccountStatus.FROZEN:
            raise errors.AccountFrozenError(
                self._account_id,
                message=f"Невозможно разморозить счет в статусе {self._status}",
            )
        self._status = AccountStatus.ACTIVE
        print(f"Счет {self._account_id} разморожен.")

    def close(self) -> None:
        self._ensure_client_status((ClientStatus.ACTIVE,))
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
