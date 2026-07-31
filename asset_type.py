from enum import Enum, unique
from typing import Union

from errors import InstanceTypeError


@unique
class AssetType(Enum):
    STOCK = "STOCK"
    BOND = "BOND"
    ETF = "ETF"

    @classmethod
    def from_str(cls, value: Union[str, "AssetType"]) -> "AssetType":
        if isinstance(value, AssetType):
            return value
        if isinstance(value, str):
            value_upper = value.upper()
            try:
                return AssetType(value_upper)
            except ValueError:
                raise InstanceTypeError(cls.__name__, value, (str, AssetType), "value")
        raise InstanceTypeError(cls.__name__, value, (str, AssetType), "value")

    def __str__(self) -> str:
        return self.value
