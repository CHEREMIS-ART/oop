from datetime import date
from typing import Union

from asset import Asset
from currency import Currency
from asset_type import AssetType
from account_status import AccountStatus
from errors import InstanceTypeError, InvalidOperationError


class Bond(Asset):
    def __init__(
        self,
        symbol: str,
        name: str,
        currency: Union[Currency, str],
        current_price: Union[float, int],
        face_value: Union[float, int],
        coupon_rate: float,
        maturity_date: date,
    ):
        super().__init__(symbol, name, AssetType.BOND, currency, current_price)
        if not isinstance(face_value, (float, int)):
            raise InstanceTypeError(
                self.__class__.__name__, face_value, (float, int), "face_value"
            )
        if face_value <= 0:
            raise InvalidOperationError(
                None, message="Номинал облигации должен быть > 0."
            )
        if not isinstance(coupon_rate, float):
            raise InstanceTypeError(
                self.__class__.__name__, coupon_rate, (float,), "coupon_rate"
            )
        if not (0 <= coupon_rate <= 1):
            raise InvalidOperationError(
                None, message="Купонная ставка должна быть в пределах [0, 1]."
            )
        if not isinstance(maturity_date, date):
            raise InstanceTypeError(
                self.__class__.__name__, maturity_date, (date,), "maturity_date"
            )
        if maturity_date < date.today():
            raise InvalidOperationError(
                None, message=f"Дата погашения должна быть позже {date.today()}"
            )
        self._face_value = face_value
        self._coupon_rate = coupon_rate
        self._maturity_date = maturity_date

    def calculate_current_yield(self) -> float:
        return (self._coupon_rate * self._face_value) / self._current_price

    def calculate_annual_coupon(self) -> float:
        return self._face_value * self._coupon_rate

    def __str__(self) -> str:
        return (
            super().__str__() + f"\n - Номинал облигации: {self._face_value}"
            f"\n - Купонная ставка в долях (годовая): {self._coupon_rate}"
            f"\n - Дата погашения: {self._maturity_date.isoformat()}"
        )
