from dataclasses import dataclass
from uuid import UUID

from dataparity.domain.dataset_version import DatasetVersion, DatasetVersionStatus


@dataclass(frozen=True)
class Dataset:
    id: UUID
    name: str
    active_baseline_version_id: UUID | None = None

    def set_active_baseline(self, version: DatasetVersion) -> "Dataset":
        if version.dataset_id != self.id:
            raise ValueError("Version does not belong to this dataset")

        if version.status != DatasetVersionStatus.APPROVED:
            raise ValueError("Only approved versions can be set as the active baseline")

        return Dataset(
            id=self.id, name=self.name, active_baseline_version_id=version.id
        )
