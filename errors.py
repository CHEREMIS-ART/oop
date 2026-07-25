class AccountError(Exception):
    def __init__(self, message):
        self.message = message


class AccountFrozenError(AccountError):
    def __init__(self, id: str, message=None):
        self.id = id
        if message is None:
            message = f"Счет ***{self.id} заморожен. Операция недоступна."
        self.message = message
        super().__init__(self.message)


class AccountClosedError(AccountError):
    def __init__(self, id: str, message=None):
        self.id = id
        if message is None:
            message = f"Счет ***{self.id} закрыт. Операция недоступна."
        self.message = message
        super().__init__(self.message)


class BalanceNotZeroError(AccountError):
    def __init__(self, id: str, message=None):
        self.id = id
        if message is None:
            message = f"Нельзя закрыть счет ***{self.id}. Ненулевой баланс."
        self.message = message
        super().__init__(self.message)


class InvalidOperationError(AccountError):
    def __init__(self, id: str, message=None):
        self.id = id
        if message is None:
            message = f"Счет ***{self.id}. Недопустимая операция."
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


class UnderageError(AccountError):
    def __init__(self, message="Клиенту нет 18 лет."):
        self.message = message
        super().__init__(self.message)
