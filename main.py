from datetime import date

from bank import Bank
from bank_account import BankAccount
from savings_account import SavingsAccount
from premium_account import PremiumAccount
from investment_account import InvestmentAccount
from client import Client
from currency import Currency
from stock import Stock
from bond import Bond
from etf import Etf
from sectors_type import SectorType
from account_type import AccountType
from errors import AccountFrozenError, BalanceNotZeroError
import errors


def test_bank():
    bank = Bank("Тестовый банк")

    client1 = Client(
        passport_series=1234,
        passport_number=567890,
        age=25,
        phone_number=123456789,
        address="ул. Ленина, 1",
        first_name="Иван",
        last_name="Петров",
    )
    client2 = Client(
        passport_series=4321,
        passport_number=987654,
        age=30,
        phone_number=987654321,
        address="ул. Пушкина, 2",
        first_name="Мария",
        last_name="Иванова",
    )
    client1.verification_client()
    client2.verification_client()
    
    bank.add_client(client1)
    bank.add_client(client2)

    acc1 = bank.open_account(client1, AccountType.SAVINGS, 1000, Currency.RUB)
    acc2 = bank.open_account(client2, AccountType.PREMIUM, 5000, Currency.USD)

    print("Баланс банка:", bank.get_total_balance())

    try:
        bank.authenticate_client(client1.get_client_id(), 1234, 567890)
        print("Клиент1 аутентифицирован успешно.")
    except Exception as e:
        print("Ошибка аутентификации:", e)

    try:
        bank.authenticate_client(client1.get_client_id(), 9999, 999999)
    except Exception as e:
        print("Ожидаемая ошибка:", e)

    try:
        bank.authenticate_client(client1.get_client_id(), 9999, 999999)
    except Exception as e:
        print("Вторая попытка:", e)
    try:
        bank.authenticate_client(client1.get_client_id(), 9999, 999999)
    except Exception as e:
        print("Третья попытка (блокировка):", e)

    print("Статус клиента1 после блокировки:", client1.get_status())

    try:
        bank.open_account(client1, AccountType.SAVINGS, 100, Currency.RUB)
    except Exception as e:
        print("Ожидаемая ошибка открытия счёта:", e)

    bank.freeze_account(acc2.get_account_id())
    print("Счёт acc2 заморожен")

    try:
        acc2.withdraw(100)
    except AccountFrozenError as e:
        print("Ошибка при снятии с замороженного счёта:", e)

    bank.unfreeze_account(acc2.get_account_id())
    print("Счёт acc2 разморожен")

    try:
        bank.close_account(acc2.get_account_id())
    except BalanceNotZeroError as e:
        print("Ошибка закрытия (баланс не нулевой):", e)

    acc2.withdraw(5000)
    bank.close_account(acc2.get_account_id())
    print("Счёт acc2 закрыт")

    print("Поиск по валюте RUB:", bank.search_accounts(currency="RUB"))
    print("Рейтинг клиентов:", bank.get_clients_ranking())


if __name__ == "__main__":
    owner = Client(1234, 7755533, 30, 123456789, "ул. Примерная, 1", "Ivan", "Ivanov")
    owner.verification_client()
    try:
        ivan_account = BankAccount(owner, 1000, Currency.RUB)
        ivan_account.deposit(500)
        ivan_account.withdraw(250)
        print(ivan_account.get_account_info())
    except errors.AccountError as error:
        print(error.message)

    owner2 = Client(4321, 5555777, 21, 987654321, "ул. Тестовая, 2", "Masha", "Frolova")
    owner2.verification_client()
    try:
        masha_account = BankAccount(owner2, 0, "usd")
        masha_account.freeze()
        masha_account.deposit(1000)
    except errors.InstanceTypeError as error:
        print(error.message)
    except errors.AccountFrozenError as error:
        print(error.message)

    masha_savings_account = SavingsAccount(owner2, 1000, "kzt", monthly_interest=1.3)
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

    masha_premium_account = PremiumAccount(owner2, 100_000, "usd")
    print(masha_premium_account.get_account_info())
    masha_premium_account.withdraw(90_000)
    masha_premium_account.withdraw(20_000)
    masha_premium_account.withdraw(90_000)
    try:
        masha_premium_account.withdraw(1000)
    except errors.InsufficientFundsError as error:
        print(str(error))
    masha_premium_account.deposit(200_000)

    owner_petr = Client(
        5678, 1234567, 25, 555123456, "ул. Петрова, 3", "Petr", "Petrov"
    )
    owner_petr.verification_client()
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

    test_bank()
