from dataclasses import dataclass
from enum import StrEnum

from dataparity.domain.column import Column


class SchemaChangeType(StrEnum):
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"


@dataclass(frozen=True)
class SchemaChange:
    type: SchemaChangeType
    column_name: str
    previous: Column | None = None
    current: Column | None = None
