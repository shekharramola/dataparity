from uuid import UUID

from fastapi import FastAPI

from dataparity.api.models import (
    CompareDatasetVersionsRequest,
    SchemaChangeResponse,
)
from dataparity.domain.column import Column
from dataparity.domain.dataset_comparison import compare_dataset_versions
from dataparity.domain.dataset_version import (
    DatasetVersion,
    DatasetVersionStatus,
)

app = FastAPI(
    title="DataParity API",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/dataset-versions/compare")
def compare(
    request: CompareDatasetVersionsRequest,
) -> list[SchemaChangeResponse]:
    baseline = DatasetVersion(
        id=UUID(request.baseline.id),
        dataset_id=UUID(request.baseline.dataset_id),
        status=DatasetVersionStatus.APPROVED,
        columns=tuple(
            Column(
                name=column.name,
                data_type=column.data_type,
                nullable=column.nullable,
            )
            for column in request.baseline.columns
        ),
    )

    current = DatasetVersion(
        id=UUID(request.current.id),
        dataset_id=UUID(request.current.dataset_id),
        status=DatasetVersionStatus.PENDING_REVIEW,
        columns=tuple(
            Column(
                name=column.name,
                data_type=column.data_type,
                nullable=column.nullable,
            )
            for column in request.current.columns
        ),
    )

    changes = compare_dataset_versions(
        baseline=baseline,
        current=current,
    )

    return [
        SchemaChangeResponse(
            type=change.type,
            column_name=change.column_name,
        )
        for change in changes
    ]
