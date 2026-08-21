from pydantic import BaseModel

from dataparity.domain.column import DataType


class ColumnRequest(BaseModel):
    name: str
    data_type: DataType
    nullable: bool


class DatasetVersionRequest(BaseModel):
    id: str
    dataset_id: str
    columns: list[ColumnRequest]


class CompareDatasetVersionsRequest(BaseModel):
    baseline: DatasetVersionRequest
    current: DatasetVersionRequest


class SchemaChangeResponse(BaseModel):
    type: str
    column_name: str
