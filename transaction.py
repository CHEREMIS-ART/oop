from datetime import datetime
from uuid import uuid4
from typing import Union, Optional, Dict

from transaction_type import TransactionType
from transaction_status import TransactionStatus
from currency import Currency
from errors import (
    InstanceTypeError,
    InvalidOperationError,
)


class Transaction:
    def __init__(
        self,
        transaction_type: TransactionType,
        amount: Union[float, int],
        currency: Union[str, Currency],
        sender_account_id: Optional[int],
        receiver_account_id: Optional[int],
        failure_reason: Optional[str],
    ):
        if not isinstance(transaction_type, (TransactionType)):
            raise InstanceTypeError(
                self.__class__.__name__,
                transaction_type,
                (TransactionType),
                "transaction_type",
            )
        if not isinstance(amount, (float, int)):
            raise InstanceTypeError(
                self.__class__.__name__, amount, (float, int), "amount"
            )
        if amount < 0:
            raise InvalidOperationError(None, message="Сумма должна быть > 0.")
        if not isinstance(currency, (str, Currency)):
            raise InstanceTypeError(
                self.__class__.__name__, currency, (str, Currency), "currency"
            )
        if sender_account_id is not None and not isinstance(sender_account_id, int):
            raise InstanceTypeError(
                self.__class__.__name__,
                sender_account_id,
                (int, None),
                "sender_account_id",
            )
        if receiver_account_id is not None and not isinstance(receiver_account_id, int):
            raise InstanceTypeError(
                self.__class__.__name__,
                receiver_account_id,
                (int,),
                "receiver_account_id",
            )
        if failure_reason is not None and not isinstance(failure_reason, str):
            raise InstanceTypeError(
                self.__class__.__name__, failure_reason, (str, None), "failure_reason"
            )

        self.__transaction_id = uuid4().int
        self.__transaction_type = transaction_type
        self.__amount = amount
        self.__currency = Currency.from_str(currency)

        self.__fee = 0.0
        self.__sender_account_id = sender_account_id
        self.__receiver_account_id = receiver_account_id
        self.__transaction_status = TransactionStatus.PENDING

        self.__failure_reason = failure_reason
        self.__attempts = 0

        self.__created_at = datetime.now()
        self.__scheduled_for = None
        self.__processed_at = None
        self.__last_attempt = None

    def set_fee(self, fee: Union[float, int]) -> None:
        if not isinstance(fee, (float, int)):
            raise InstanceTypeError(self.__class__.__name__, fee, (float, int), "fee")
        self.__fee = fee

    def get_status(self) -> TransactionStatus:
        return self.__transaction_status

    def set_status(self, new_status: TransactionStatus) -> None:
        if not isinstance(new_status, TransactionStatus):
            raise InstanceTypeError(
                self.__class__.__name__, new_status, (TransactionStatus,), "new_status"
            )
        self.__transaction_status = new_status
