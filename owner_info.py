class OwnerInfo:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        age: int,
        passport_series: int,
        passport_number: int,
    ) -> None:

        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.__passport_series = passport_series
        self.__passport_number = passport_number

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} age: {self.age}"
