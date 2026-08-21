from uuid import uuid4

from dataparity.domain.dataset import Dataset
from dataparity.domain.dataset_version import DatasetVersion, DatasetVersionStatus


def test_new_dataset_has_no_active_baseline():
    dataset = Dataset(
        id=uuid4(),
        name="Supplier master data",
    )
    assert dataset.active_baseline_version_id is None


def test_dataset_can_set_approved_version_as_active_baseline():
    dataset = Dataset(
        id=uuid4(),
        name="Supplier master data",
    )

    version = DatasetVersion(
        id=uuid4(), dataset_id=dataset.id, status=DatasetVersionStatus.PENDING_REVIEW
    )

    approved_version = version.approve()

    updated_dataset = dataset.set_active_baseline(approved_version)

    assert dataset.active_baseline_version_id is None

    assert updated_dataset.active_baseline_version_id == approved_version.id
