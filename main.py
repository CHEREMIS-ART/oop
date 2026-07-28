from bank_account import BankAccount
from savings_account import SavingsAccount
from premium_account import PremiumAccount
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

    masha_savings_account = SavingsAccount(owner, 1000, "kzt", monthly_interest=1.3)
    masha_savings_account.deposit(250)
    masha_savings_account.withdraw(1150)
    masha_savings_account.deposit(2900)
    masha_savings_account.freeze()
    try:
        masha_savings_account.apply_monthly_interest()
    except errors.AccountError as error:
        print(error)
    masha_savings_account.get_account_info()
    print(masha_savings_account)

    masha_premium_account = PremiumAccount(owner, 100_000, "usd")
    print(masha_premium_account.get_account_info())
    masha_premium_account.withdraw(90_000)
    masha_premium_account.withdraw(20_000)
    masha_premium_account.withdraw(90_000)
    try:
        masha_premium_account.withdraw(1000)
    except errors.InsufficientFundsError as error:
        print(str(error))
    masha_premium_account.deposit(200_000)
