from bank_account import BankAccount
from owner_info import OwnerInfo
from currency import Currency
import errors


if __name__ == "__main__":
    owner = OwnerInfo("Ivan", "Ivanov", 30, 1234, 7755533)
    ivan_account = BankAccount(owner, 1000, Currency.RUB)

    owner = OwnerInfo("Masha", "Frolova", 21, 4321, 5555777)
    masha_account = BankAccount(owner, 0, Currency.EUR)
    masha_account.freeze()

    try:
        masha_account.deposit(1000)
    except errors.AccountFrozenError as error:
        print(error.message)
    
    try:
        ivan_account.deposit(500)
        ivan_account.withdraw(250)
        print(ivan_account.get_account_info())
    except errors.AccountError as error:
        print(error.message)