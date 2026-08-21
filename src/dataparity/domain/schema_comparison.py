from dataparity.domain.column import Column
from dataparity.domain.schema_change import SchemaChange, SchemaChangeType


def compare_schemas(
    baseline: tuple[Column, ...],
    current: tuple[Column, ...],
) -> tuple[SchemaChange, ...]:
    baseline_by_name = {column.name: column for column in baseline}
    current_by_name = {column.name: column for column in current}

    changes: list[SchemaChange] = []

    for name, column in current_by_name.items():
        baseline_column = baseline_by_name.get(name)

        if baseline_column is None:
            changes.append(
                SchemaChange(
                    type=SchemaChangeType.ADDED,
                    column_name=name,
                    current=column,
                )
            )
        elif baseline_column != column:
            changes.append(
                SchemaChange(
                    type=SchemaChangeType.MODIFIED,
                    column_name=name,
                    previous=baseline_column,
                    current=column,
                )
            )

    for name, column in baseline_by_name.items():
        if name not in current_by_name:
            changes.append(
                SchemaChange(
                    type=SchemaChangeType.REMOVED,
                    column_name=name,
                    previous=column,
                )
            )

    return tuple(changes)
