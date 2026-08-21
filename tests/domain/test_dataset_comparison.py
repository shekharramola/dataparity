from uuid import uuid4

import pytest

from dataparity.domain.column import Column, DataType
from dataparity.domain.dataset_comparison import compare_dataset_versions
from dataparity.domain.dataset_version import DatasetVersion, DatasetVersionStatus
from dataparity.domain.schema_change import SchemaChangeType


def test_compares_versions_from_same_dataset():
    dataset_id = uuid4()

    baseline = DatasetVersion(
        id=uuid4(),
        dataset_id=dataset_id,
        status=DatasetVersionStatus.APPROVED,
        columns=(
            Column(
                name="supplier_id",
                data_type=DataType.INTEGER,
                nullable=False,
            ),
        ),
    )

    current = DatasetVersion(
        id=uuid4(),
        dataset_id=dataset_id,
        status=DatasetVersionStatus.PENDING_REVIEW,
        columns=(
            Column(
                name="supplier_id",
                data_type=DataType.INTEGER,
                nullable=False,
            ),
            Column(
                name="email",
                data_type=DataType.STRING,
                nullable=True,
            ),
        ),
    )

    changes = compare_dataset_versions(baseline, current)

    assert len(changes) == 1
    assert changes[0].type == SchemaChangeType.ADDED
    assert changes[0].column_name == "email"


def test_cannot_compare_versions_from_different_datasets():
    baseline = DatasetVersion(
        id=uuid4(),
        dataset_id=uuid4(),
        status=DatasetVersionStatus.APPROVED,
    )

    current = DatasetVersion(
        id=uuid4(),
        dataset_id=uuid4(),
        status=DatasetVersionStatus.PENDING_REVIEW,
    )

    with pytest.raises(ValueError):
        compare_dataset_versions(baseline, current)
