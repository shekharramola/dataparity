from dataparity.domain.column import Column, DataType
from dataparity.domain.schema_change import SchemaChangeType
from dataparity.domain.schema_comparison import compare_schemas


def test_detects_added_column():
    current_column = Column(
        name="email",
        data_type=DataType.STRING,
        nullable=True,
    )

    changes = compare_schemas(
        baseline=(),
        current=(current_column,),
    )

    assert len(changes) == 1

    change = changes[0]

    assert change.type == SchemaChangeType.ADDED
    assert change.column_name == "email"
    assert change.previous is None
    assert change.current == current_column


def test_detects_removed_column():
    baseline_column = Column(
        name="country",
        data_type=DataType.STRING,
        nullable=True,
    )

    changes = compare_schemas(
        baseline=(baseline_column,),
        current=(),
    )

    assert len(changes) == 1

    change = changes[0]

    assert change.type == SchemaChangeType.REMOVED
    assert change.column_name == "country"
    assert change.previous == baseline_column
    assert change.current is None


def test_detects_modified_column():
    baseline_column = Column(
        name="supplier_name",
        data_type=DataType.STRING,
        nullable=False,
    )

    current_column = Column(
        name="supplier_name",
        data_type=DataType.STRING,
        nullable=True,
    )

    changes = compare_schemas(
        baseline=(baseline_column,),
        current=(current_column,),
    )

    assert len(changes) == 1

    change = changes[0]

    assert change.type == SchemaChangeType.MODIFIED
    assert change.column_name == "supplier_name"
    assert change.previous == baseline_column
    assert change.current == current_column
