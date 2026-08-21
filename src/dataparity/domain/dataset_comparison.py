from dataparity.domain.dataset_version import DatasetVersion
from dataparity.domain.schema_change import SchemaChange
from dataparity.domain.schema_comparison import compare_schemas


def compare_dataset_versions(
    baseline: DatasetVersion,
    current: DatasetVersion,
) -> tuple[SchemaChange, ...]:
    if baseline.dataset_id != current.dataset_id:
        raise ValueError("Dataset versions must belong to the same dataset")

    return compare_schemas(
        baseline=baseline.columns,
        current=current.columns,
    )
