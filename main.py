from bank_account import BankAccount
from owner_info import OwnerInfo
from currency import Currency
import errors


if __name__ == "__main__":
    owner = OwnerInfo("Ivan", "Ivanov", 30, 1234, 7755533)
    try:
        ivan_account = BankAccount(owner, 1000, Currency.RUB)
        ivan_account.deposit(500)
        ivan_account.withdraw(250)
        print(ivan_account.get_account_info())
    except errors.CurrencyError as error:
        print(error.message)
    except errors.AccountError as error:
        print(error.message)

    owner = OwnerInfo("Masha", "Frolova", 21, 4321, 5555777)
    try:
        masha_account = BankAccount(owner, 0, "usd")
        masha_account.freeze()
        masha_account.deposit(1000)
    except errors.CurrencyError as error:
        print(error.message)
    except errors.AccountFrozenError as error:
        print(error.message)
