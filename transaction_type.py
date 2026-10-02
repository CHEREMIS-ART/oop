from enum import Enum, unique


@unique
class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    INTERNAL_TRANSFER = "INTERNAL TRANSFER"
    EXTERNAL_TRANSFER = "EXTERNAL TRANSFER"
    INVESTMENT_BUY_SELL = "INVESTMENT BUY/SELL"

    def __str__(self) -> str:
        return self.value
