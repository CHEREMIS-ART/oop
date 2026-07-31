class OwnerInfo:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        age: int,
        passport_series: int,
        passport_number: int,
    ) -> None:

        self._first_name = first_name
        self._last_name = last_name
        self._age = age
        self.__passport_series = passport_series
        self.__passport_number = passport_number

    def __str__(self) -> str:
        return f"{self._first_name} {self._last_name} age: {self._age}"
