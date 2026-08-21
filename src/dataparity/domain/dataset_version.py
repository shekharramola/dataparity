from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

from dataparity.domain.column import Column


class DatasetVersionStatus(StrEnum):
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass(frozen=True)
class DatasetVersion:
    id: UUID
    dataset_id: UUID
    status: DatasetVersionStatus
    columns: tuple[Column, ...] = ()
    rejection_reason: str | None = None

    def approve(self) -> "DatasetVersion":
        if self.status != DatasetVersionStatus.PENDING_REVIEW:
            raise ValueError("Only pending versions can be approved")

        return DatasetVersion(
            id=self.id,
            dataset_id=self.dataset_id,
            status=DatasetVersionStatus.APPROVED,
            columns=self.columns,
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
            columns=self.columns,
            rejection_reason=reason,
        )
