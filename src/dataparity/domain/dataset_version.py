from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class DatasetVersionStatus(str, Enum):
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass(frozen=True)
class DatasetVersion:
    id: UUID
    dataset_id: UUID
    status: DatasetVersionStatus