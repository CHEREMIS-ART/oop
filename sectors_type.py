from enum import Enum, unique
from typing import Union

from errors import InstanceTypeError


@unique
class SectorType(Enum):
    INFORMATION_TECHNOLOGY = "Information Technology"
    HEALTH_CARE = "Health Care"
    FINANCIALS = "Financials"
    CONSUMER_DISCRETIONARY = "Consumer Discretionary"
    COMMUNICATION_SERVICES = "Communication Services"
    INDUSTRIALS = "Industrials"
    CONSUMER_STAPLES = "Consumer Staples"
    ENERGY = "Energy"
    UTILITIES = "Utilities"
    REAL_ESTATE = "Real Estate"
    MATERIALS = "Materials"

    @classmethod
    def from_str(cls, value: Union[str, "SectorType"]) -> "SectorType":
        if isinstance(value, SectorType):
            return value
        if isinstance(value, str):
            value_title = value.title()
            try:
                return SectorType(value_title)
            except ValueError:
                raise InstanceTypeError(cls.__name__, value, (str, SectorType), "value")
        raise InstanceTypeError(cls.__name__, value, (str, SectorType), "value")

    def __str__(self) -> str:
        return self.value
