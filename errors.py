from typing import Any


class AccountError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class AccountFrozenError(AccountError):
    def __init__(self, id: str, message=None):
        self.id = id
        if message is None:
            message = f"Счет {self.id} заморожен. Операция недоступна."
        self.message = message
        super().__init__(self.message)


class AccountClosedError(AccountError):
    def __init__(self, id: str, message=None):
        self.id = id
        if message is None:
            message = f"Счет {self.id} закрыт. Операция недоступна."
        self.message = message
        super().__init__(self.message)


class BalanceNotZeroError(AccountError):
    def __init__(self, id: str, message=None):
        self.id = id
        if message is None:
            message = f"Нельзя закрыть счет {self.id}. Ненулевой баланс."
        self.message = message
        super().__init__(self.message)


class InvalidOperationError(AccountError):
    def __init__(self, id: str, message=None):
        self.id = id
        if message is None:
            message = f"Счет {self.id}. Недопустимая операция."
        self.message = message
        super().__init__(self.message)


class InsufficientFundsError(AccountError):
    def __init__(self, balance: float, amount: float, message=None):
        self.balance = balance
        self.amount = amount
        if message is None:
            message = f"Недостаточно средств. Баланс: {balance}, запрошено: {amount}"
        self.message = message
        super().__init__(self.message)


class InstanceTypeError(AccountError):
    def __init__(
        self,
        class_name: str,
        value: Any,
        expected_type: tuple[type] = None,
        var_name: str = None,
        message=None,
    ):
        self.class_name = class_name
        self.value = value
        self.expected_type = expected_type
        self.var_name = var_name
        if message is None:
            type_names = ", ".join(t.__name__ for t in expected_type)
            actual_type = type(value).__name__
            if self.var_name:
                message = f"Класс: {self.class_name}. Ожидается для {self.var_name} тип: {type_names}. Передан тип: {actual_type}"
            else:
                message = f"Класс: {self.class_name}. Ожидается тип: {type_names}. Передан тип: {actual_type}"
        self.message = message
        super().__init__(self.message)


class DuplicateAccountError(AccountError):
    def __init__(self, id: str, message=None):
        self.id = id
        if message is None:
            message = f"Счёт {self.id} уже добавлен клиенту."
        self.message = message
        super().__init__(self.message)


class OperationTimeRestrictedError(AccountError):
    def __init__(self, message="Операции запрещены с 00:00 до 05:00."):
        self.message = message
        super().__init__(self.message)


class ClientError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UnderageError(ClientError):
    def __init__(self, message="Клиенту нет 18 лет."):
        self.message = message
        super().__init__(self.message)


class NumberOfAccountsError(ClientError):
    def __init__(self, message="У клиента есть еще счета."):
        self.message = message
        super().__init__(self.message)


class ClientFrozenError(ClientError):
    def __init__(self, message="Клиент заблокирован. Операции со счетами недоступны."):
        self.message = message
        super().__init__(self.message)


class ClientClosedError(ClientError):
    def __init__(self, message="Клиент закрыт. Все счета клиента закрыты."):
        self.message = message
        super().__init__(self.message)


class ClientRestrictedError(ClientError):
    def __init__(
        self, message="Клиент ограничен в доступе. Возможно только пополнение счетов."
    ):
        self.message = message
        super().__init__(self.message)


class ClientNotVerifiedError(ClientError):
    def __init__(
        self, message="Клиент еще не верифицирован. Операции со счетами недоступны."
    ):
        self.message = message
        super().__init__(self.message)


class ClientStatusTypeError(ClientError):
    def __init__(self, message="Неизвестный статус клиента."):
        self.message = message
        super().__init__(self.message)


class DuplicateClientError(ClientError):
    def __init__(self, id: str, message=None):
        self.id = id
        if message is None:
            message = f"Клиент {self.id} уже обслуживается банком."
        self.message = message
        super().__init__(self.message)
