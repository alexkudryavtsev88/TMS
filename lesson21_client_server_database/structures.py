from dataclasses import dataclass, asdict
from enum import Enum


@dataclass(frozen=True)
class User:
    name: str
    age: int
    gender: str
    nationality: str = "belarus"

    def to_dict(self):
        return asdict(self)


class OperationStatus(str, Enum):
    SUCCESS = "SUCCESS"
    NOT_EXIST = "NOT EXIST"
    NOT_UNIQUE = "NOT UNIQUE"
