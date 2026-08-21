from uuid import uuid4

import pytest

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


def test_pending_version_cannot_be_set_as_active_baseline():
    dataset = Dataset(id=uuid4(), name="Supplier master data")
    version = DatasetVersion(
        id=uuid4(), dataset_id=dataset.id, status=DatasetVersionStatus.PENDING_REVIEW
    )

    with pytest.raises(
        ValueError, match="Only approved versions can be set as the active baseline"
    ):
        dataset.set_active_baseline(version)


def test_version_from_another_dataset_cannot_be_set_as_active_baseline():
    dataset = Dataset(id=uuid4(), name="Supplier master data")
    version = DatasetVersion(
        id=uuid4(), dataset_id=uuid4(), status=DatasetVersionStatus.APPROVED
    )

    with pytest.raises(ValueError, match="Version does not belong to this dataset"):
        dataset.set_active_baseline(version)


def test_approved_version_can_replace_current_active_baseline():
    dataset = Dataset(
        id=uuid4(),
        name="Supplier master data",
    )

    first_version = DatasetVersion(
        id=uuid4(),
        dataset_id=dataset.id,
        status=DatasetVersionStatus.APPROVED,
    )

    second_version = DatasetVersion(
        id=uuid4(),
        dataset_id=dataset.id,
        status=DatasetVersionStatus.APPROVED,
    )

    dataset_with_first_baseline = dataset.set_active_baseline(first_version)
    updated_dataset = dataset_with_first_baseline.set_active_baseline(second_version)

    assert dataset_with_first_baseline.active_baseline_version_id == first_version.id
    assert updated_dataset.active_baseline_version_id == second_version.id


def test_approving_a_new_version_does_not_change_current_active_baseline():
    dataset = Dataset(
        id=uuid4(),
        name="Supplier master data",
    )

    first_version = DatasetVersion(
        id=uuid4(),
        dataset_id=dataset.id,
        status=DatasetVersionStatus.APPROVED,
    )

    dataset_with_baseline = dataset.set_active_baseline(first_version)

    pending_version = DatasetVersion(
        id=uuid4(),
        dataset_id=dataset.id,
        status=DatasetVersionStatus.PENDING_REVIEW,
    )

    approved_version = pending_version.approve()

    assert dataset_with_baseline.active_baseline_version_id == first_version.id
    assert approved_version.status == DatasetVersionStatus.APPROVED
    assert approved_version.id != dataset_with_baseline.active_baseline_version_id
