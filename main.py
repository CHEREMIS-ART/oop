from datetime import date

from bank_account import BankAccount
from savings_account import SavingsAccount
from premium_account import PremiumAccount
from investment_account import InvestmentAccount
from owner_info import OwnerInfo
from currency import Currency
from stock import Stock
from bond import Bond
from etf import Etf
from sectors_type import SectorType
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
    except errors.InstanceTypeError as error:
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

    owner_petr = OwnerInfo("Petr", "Petrov", 25, 5678, 1234567)
    petr_ivest_account = InvestmentAccount(owner_petr, 50_000, Currency.RUB)
    print(petr_ivest_account)

    stock1 = Stock(
        "YNDX", "Yandex", "RUB", 5000.0, 0.02, SectorType.INFORMATION_TECHNOLOGY
    )
    stock2 = Stock("GAZP", "Gazprom", "RUB", 200.0, 0.06, SectorType.ENERGY)
    bond1 = Bond(
        "OFZ26233", "ОФЗ 26233", "RUB", 980.0, 1000.0, 0.07, date(2030, 12, 15)
    )
    etf1 = Etf(
        "FXRL",
        "ETF на российские акции",
        "RUB",
        1500.0,
        0.009,
        {
            "YNDX": {"asset": stock1, "weight": 0.4},
            "GAZP": {"asset": stock2, "weight": 0.6},
        },
    )

    try:
        petr_ivest_account.buy_asset(stock1, 5)
        petr_ivest_account.buy_asset(stock2, 100)
        petr_ivest_account.buy_asset(bond1, 10)
        petr_ivest_account.buy_asset(etf1, 3)
    except errors.AccountError as e:
        print(f"Ошибка при покупке: {e}")

    print(petr_ivest_account)

    try:
        petr_ivest_account.accrue_income(30)
    except errors.AccountError as e:
        print(f"Ошибка при начислении дохода: {e}")

    try:
        petr_ivest_account.sell_asset("YNDX", 2)
    except errors.AccountError as e:
        print(f"Ошибка при продаже: {e}")

    print(petr_ivest_account)

    try:
        petr_ivest_account.sell_asset("YNDX", 10)
    except errors.AccountError as e:
        print(f"\nОжидаемая ошибка при продаже: {e}")

    try:
        petr_ivest_account.buy_asset(stock1, 1000)
    except errors.AccountError as e:
        print(f"Ожидаемая ошибка при покупке: {e}")

    try:
        petr_ivest_account.close()
    except errors.AccountError as e:
        print(f"\nОжидаемая ошибка при закрытии (баланс не нулевой): {e}")
