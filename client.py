from uuid import uuid4
from typing import List

from client_status import ClientStatus
import errors


class Client:
    def __init__(
        self,
        passport_series: int,
        passport_number: int,
        age: int,
        phone_number: int,
        address: str,
        first_name: str,
        last_name: str,
        middle_name: str = None,
        email: str = None,
        client_id: int = None,
    ) -> None:
        if not isinstance(passport_series, int):
            raise errors.InstanceTypeError(
                self.__class__.__name__, passport_series, (int,), "passport_series"
            )
        if not isinstance(passport_number, int):
            raise errors.InstanceTypeError(
                self.__class__.__name__, passport_number, (int,), "passport_number"
            )
        if not isinstance(age, int):
            raise errors.InstanceTypeError(self.__class__.__name__, age, (int,), "age")
        if age < 18:
            raise errors.UnderageError()
        if not isinstance(phone_number, int):
            raise errors.InstanceTypeError(
                self.__class__.__name__, phone_number, (int,), "phone_number"
            )
        if not isinstance(address, str):
            raise errors.InstanceTypeError(
                self.__class__.__name__, address, (str,), "address"
            )
        if not isinstance(first_name, str):
            raise errors.InstanceTypeError(
                self.__class__.__name__, first_name, (str,), "first_name"
            )
        if not isinstance(last_name, str):
            raise errors.InstanceTypeError(
                self.__class__.__name__, first_name, (str,), "last_name"
            )
        self.__passport_series = passport_series
        self.__passport_number = passport_number
        self.__age = age
        self.__phone_number = phone_number
        self.__address = address
        self.__first_name = first_name
        self.__last_name = last_name
        if middle_name is not None:
            if not isinstance(middle_name, str):
                raise errors.InstanceTypeError(
                    self.__class__.__name__, middle_name, (str,), "middle_name"
                )
        self.__middle_name = middle_name
        if email is not None:
            if not isinstance(email, str):
                raise errors.InstanceTypeError(
                    self.__class__.__name__, email, (str,), "email"
                )
        self.__email = email
        if client_id is None:
            client_id = uuid4().int
        self.__client_id = client_id
        self.__status = ClientStatus.PENDING_VERIFICATION
        self.__accounts: List[int] = []
        self._failed_login_attempts = 0
        self._suspicious_activities: List[str] = []

    def get_status(self) -> ClientStatus:
        return self.__status

    def get_account_ids(self) -> list[int]:
        return self.__accounts

    def get_client_id(self) -> int:
        return self.__client_id

    def verification_client(self) -> None:
        if self.__status == ClientStatus.PENDING_VERIFICATION:
            self.__status = ClientStatus.ACTIVE
        else:
            raise errors.ClientStatusTypeError(
                message=f"Для текущего статуса клиента: {self.__status} верификация ненужна."
            )

    def freeze_client(self) -> None:
        if self.__status == ClientStatus.FROZEN:
            raise errors.ClientFrozenError(message="Клиент уже заблокирован.")
        if self.__status == ClientStatus.ACTIVE:
            self.__status = ClientStatus.FROZEN
        else:
            raise errors.ClientStatusTypeError(
                message=f"Для текущего статуса клиента: {self.__status} блокировка невозможна."
            )

    def unfreeze(self) -> None:
        if (
            self.__status == ClientStatus.FROZEN
            or self.__status == ClientStatus.RESTRICTED
        ):
            self.__status = ClientStatus.ACTIVE
        else:
            raise errors.ClientStatusTypeError(
                message=f"Для текущего статуса клиента: {self.__status} разблокировка невозможна."
            )

    def close_client(self) -> None:
        if self.__status == ClientStatus.ACTIVE:
            if len(self.__accounts) != 0:
                raise errors.NumberOfAccountsError()
            self.__status = ClientStatus.CLOSED
        else:
            raise errors.ClientStatusTypeError(
                message=f"Для текущего статуса клиента: {self.__status} закрытие невозможно."
            )

    def restricted_client(self) -> None:
        if self.__status == ClientStatus.ACTIVE:
            self.__status = ClientStatus.RESTRICTED
        else:
            raise errors.ClientStatusTypeError(
                message=f"Для текущего статуса клиента: {self.__status} ограничение невозможно."
            )

    def add_account(self, new_account_id: int) -> None:
        if self.__status == ClientStatus.FROZEN:
            raise errors.ClientFrozenError()
        if self.__status == ClientStatus.CLOSED:
            raise errors.ClientClosedError()
        if self.__status == ClientStatus.PENDING_VERIFICATION:
            raise errors.ClientNotVerifiedError()
        if self.__status == ClientStatus.RESTRICTED:
            raise errors.ClientRestrictedError()
        if self.__status == ClientStatus.ACTIVE:
            if not isinstance(new_account_id, int):
                raise errors.InstanceTypeError(
                    self.__class__.__name__, new_account_id, (int,), "new_account_id"
                )
            if new_account_id <= 0:
                raise errors.InvalidOperationError(None, "Номер счета должен быть > 0.")
            for account_id in self.__accounts:
                if account_id == new_account_id:
                    raise errors.DuplicateAccountError(new_account_id)
            self.__accounts.append(new_account_id)
        else:
            raise errors.ClientStatusTypeError()

    def increment_failed_attempts(self) -> None:
        self._failed_login_attempts += 1

    def reset_failed_attempts(self) -> None:
        self._failed_login_attempts = 0

    def get_failed_attempts(self) -> int:
        return self._failed_login_attempts

    def add_suspicious_activity(self, message: str) -> None:
        self._suspicious_activities.append(message)

    def get_suspicious_activities(self) -> list:
        return self._suspicious_activities

    def get_passport_series(self) -> int:
        return self.__passport_series

    def get_passport_number(self) -> int:
        return self.__passport_number

    def __str__(self) -> str:
        return f"{self.__first_name} {self.__last_name} возраст: {self.__age} статус: "
