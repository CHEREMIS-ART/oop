from enum import Enum, unique


@unique
class TransactionStatus(Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    SCHEDULED = "SCHEDULED"

    def __str__(self) -> str:
        return self.value
