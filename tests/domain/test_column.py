from dataparity.domain.column import Column, DataType


def test_column_can_be_created():
    column = Column(name="supplier_id", data_type=DataType.INTEGER, nullable=False)

    assert column.name == "supplier_id"
    assert column.data_type == DataType.INTEGER
    assert column.nullable is False


def test_column_is_immutable():
    column = Column(name="supplier_id", data_type=DataType.INTEGER, nullable=False)

    assert column.name == "supplier_id"
