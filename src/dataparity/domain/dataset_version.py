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
    rejection_reason: str | None = None

    def approve(self) -> "DatasetVersion":
        if self.status != DatasetVersionStatus.PENDING_REVIEW:
            raise ValueError("Only pending versions can be approved")

        return DatasetVersion(
            id=self.id,
            dataset_id=self.dataset_id,
            status=DatasetVersionStatus.APPROVED,
            rejection_reason=None,
        )

    def reject(self, reason: str) -> "DatasetVersion":
        if self.status != DatasetVersionStatus.PENDING_REVIEW:
            raise ValueError("Only pending versions can be rejected")

        if not reason.strip():
            raise ValueError("Rejection reason is required")

        return DatasetVersion(
            id=self.id,
            dataset_id=self.dataset_id,
            status=DatasetVersionStatus.REJECTED,
            rejection_reason=reason,
        )
