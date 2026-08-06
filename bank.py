from typing import Union, Optional, Dict, List, Tuple, Any
from datetime import datetime

from bank_account import BankAccount
from investment_account import InvestmentAccount
from premium_account import PremiumAccount
from savings_account import SavingsAccount
from account_type import AccountType
from currency import Currency
from client import Client
from client_status import ClientStatus
from account_status import AccountStatus
from errors import (
    InstanceTypeError,
    InvalidOperationError,
    DuplicateClientError,
    ClientFrozenError,
    ClientClosedError,
    ClientNotVerifiedError,
    ClientStatusTypeError,
    AccountFrozenError,
    AccountClosedError,
    OperationTimeRestrictedError,
)


class Bank:
    def __init__(self, name: str):
        self.name = name
        self.__clients: List[Client] = []
        self.__accounts: Dict[int, BankAccount] = {}

    def _find_client_by_id(self, client_id: int) -> Optional[Client]:
        if not isinstance(client_id, int):
            raise InstanceTypeError(
                self.__class__.__name__, client_id, (int,), "client_id"
            )
        if client_id <= 0:
            raise InvalidOperationError(None, message="Номер клиента должен быть > 0.")
        for client in self.__clients:
            if client.get_client_id() == client_id:
                return client
        return None

    def _find_account(self, account_id: int) -> Optional[BankAccount]:
        if not isinstance(account_id, int):
            raise InstanceTypeError(
                self.__class__.__name__, account_id, (int,), "account_id"
            )
        if account_id <= 0:
            raise InvalidOperationError(None, message="Номер счета должен быть > 0.")
        return self.__accounts.get(account_id)

    def _get_client_for_account(self, account_id: int) -> Optional[Client]:
        account = self._find_account(account_id)
        if account:
            return account.get_account_client()
        return None

    def _check_operation_time(self) -> None:
        now = datetime.now().time()
        if now.hour < 5:
            raise OperationTimeRestrictedError()

    def _ensure_client_active(self, client: Client) -> None:
        if not isinstance(client, Client):
            raise InstanceTypeError(
                self.__class__.__name__, client, (Client,), "client"
            )
        status = client.get_status()
        if status == ClientStatus.FROZEN:
            raise ClientFrozenError()
        if status == ClientStatus.CLOSED:
            raise ClientClosedError()
        if status == ClientStatus.PENDING_VERIFICATION:
            raise ClientNotVerifiedError()
        if status != ClientStatus.ACTIVE:
            raise ClientStatusTypeError(f"Статус клиента {status} не разрешён.")

    def add_client(self, new_client: Client):
        self._check_operation_time()
        if not isinstance(new_client, Client):
            raise InstanceTypeError(
                self.__class__.__name__, new_client, (Client,), "new_client"
            )
        for client in self.__clients:
            if client.get_client_id() == new_client.get_client_id():
                raise DuplicateClientError(new_client.get_client_id())
        self.__clients.append(new_client)

    def open_account(
        self,
        client: Client,
        account_type: Union[AccountType, str],
        balance: Union[float, int],
        currency: Union[Currency, str],
    ) -> BankAccount:
        self._check_operation_time()
        if client not in self.__clients:
            raise InvalidOperationError(None, "Клиент не зарегистрирован в банке.")
        self._ensure_client_active(client)

        if account_type == AccountType.INVESTMENT:
            account = InvestmentAccount(client, balance, currency)
        elif account_type == AccountType.PREMIUM:
            account = PremiumAccount(client, balance, currency)
        elif account_type == AccountType.SAVINGS:
            account = SavingsAccount(client, balance, currency)
        else:
            raise InvalidOperationError(None, "Неизвестный тип счета.")

        account_id = account.get_account_id()
        if account_id in self.__accounts:
            raise InvalidOperationError(None, f"Счёт {account_id} уже существует.")
        self.__accounts[account_id] = account

        client.add_account(account_id)
        return account

    def close_account(self, account_id: int) -> None:
        self._check_operation_time()
        account = self._find_account(account_id)
        if not account:
            raise InvalidOperationError(account_id, "Счёт не найден.")
        client = self._get_client_for_account(account_id)
        if not client:
            raise InvalidOperationError(account_id, "Владелец счёта не найден.")
        self._ensure_client_active(client)
        account.close()

    def freeze_account(self, account_id: int) -> None:
        self._check_operation_time()
        account = self._find_account(account_id)
        if not account:
            raise InvalidOperationError(account_id, "Счёт не найден.")
        client = self._get_client_for_account(account_id)
        if not client:
            raise InvalidOperationError(account_id, "Владелец счёта не найден.")
        self._ensure_client_active(client)
        account.freeze()

    def unfreeze_account(self, account_id: int) -> None:
        self._check_operation_time()
        account = self._find_account(account_id)
        if not account:
            raise InvalidOperationError(account_id, "Счёт не найден.")
        client = self._get_client_for_account(account_id)
        if not client:
            raise InvalidOperationError(account_id, "Владелец счёта не найден.")
        account.unfreeze()

    def authenticate_client(
        self, client_id: int, passport_series: int, passport_number: int
    ) -> bool:
        client = self._find_client_by_id(client_id)
        if not client:
            raise InvalidOperationError(None, f"Клиент с ID {client_id} не найден.")

        if client.get_status() == ClientStatus.FROZEN:
            raise ClientFrozenError()

        if (
            client.get_passport_series() == passport_series
            and client.get_passport_number() == passport_number
        ):
            client.reset_failed_attempts()
            return True
        else:
            client.increment_failed_attempts()
            attempts = client.get_failed_attempts()
            client.add_suspicious_activity(
                f"Неудачная попытка входа (попытка {attempts}) в {datetime.now()}"
            )
            if attempts >= 3:
                client.freeze_client()
                client.add_suspicious_activity(
                    f"Клиент заблокирован после {attempts} неудачных попыток входа."
                )
                raise ClientFrozenError(
                    "Клиент заблокирован из-за трёх неудачных попыток входа."
                )
            raise InvalidOperationError(None, "Неверные паспортные данные.")

    def search_accounts(self, **criteria) -> List[BankAccount]:
        results = list(self.__accounts.values())
        if "client_id" in criteria:
            client_id = criteria["client_id"]
            client = self._find_client_by_id(client_id)
            if not client:
                return []
            account_ids = set(client.get_account_ids())
            results = [acc for acc in results if acc.get_account_id() in account_ids]
        if "status" in criteria:
            status = AccountStatus.from_str(criteria["status"])
            results = [acc for acc in results if acc._status == status]
        if "currency" in criteria:
            currency = Currency.from_str(criteria["currency"])
            results = [acc for acc in results if acc._currency == currency]
        if "account_type" in criteria:
            type_name = criteria["account_type"]
            results = [
                acc
                for acc in results
                if acc.__class__.__name__.lower() == type_name.lower()
            ]
        return results

    def get_total_balance(self) -> float:
        total = 0.0
        for acc in self.__accounts.values():
            total += acc._balance
        return total

    def get_clients_ranking(self) -> List[Tuple[Client, float]]:
        ranking = []
        for client in self.__clients:
            total = 0.0
            for acc_id in client.get_account_ids():
                acc = self.__accounts.get(acc_id)
                if acc:
                    total += acc._balance
            ranking.append((client, total))
        ranking.sort(key=lambda x: x[1], reverse=True)
        return ranking
