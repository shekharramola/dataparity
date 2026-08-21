from fastapi.testclient import TestClient

from dataparity.api.app import app


def test_compare_dataset_versions_detects_added_column():
    client: TestClient = TestClient(app)

    response = client.post(
        "/dataset-versions/compare",
        json={
            "baseline": {
                "id": "11111111-1111-1111-1111-111111111111",
                "dataset_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "columns": [
                    {
                        "name": "supplier_id",
                        "data_type": "integer",
                        "nullable": False,
                    },
                ],
            },
            "current": {
                "id": "22222222-2222-2222-2222-222222222222",
                "dataset_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "columns": [
                    {
                        "name": "supplier_id",
                        "data_type": "integer",
                        "nullable": False,
                    },
                    {
                        "name": "email",
                        "data_type": "string",
                        "nullable": True,
                    },
                ],
            },
        },
    )

    assert response.status_code == 200

    assert response.json() == [
        {
            "type": "added",
            "column_name": "email",
        },
    ]
