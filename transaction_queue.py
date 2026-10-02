"""
TransactionQueue
- ➕ добавление
- ⭐️ приоритет
- ⏳ отложенные операции
- ❌ отмена
"""

class TransactionQueue:
    def __init__(self):
        self.__priority = 0

    def cancel_transaction(self):
        pass