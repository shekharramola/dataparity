from dataclasses import dataclass
from enum import StrEnum


class DataType(StrEnum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"


@dataclass(frozen=True)
class Column:
    name: str
    data_type: DataType
    nullable: bool
