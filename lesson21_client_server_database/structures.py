from dataclasses import dataclass, asdict
from enum import Enum


@dataclass(frozen=True)
class User:
    name: str
    age: int

    def to_dict(self):
        return asdict(self)


class OperationStatus(str, Enum):
    SUCCESS = "SUCCESS"
    NOT_EXIST = "NOT EXIST"
    NOT_UNIQUE = "NOT UNIQUE"


class YearMonth(Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3

# month = YearMonth.JANUARY
# print(type(month))
# print(month.name)
# print(month.value)


