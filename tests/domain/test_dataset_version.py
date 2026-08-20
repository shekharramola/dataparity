from uuid import uuid4

from dataparity.domain.dataset_version import ( 
    DatasetVersion,
    DatasetVersionStatus,
)

def test_pending_version_can_be_approved():
    version = DatasetVersion(
        id=uuid4(),
        dataset_id=uuid4(),
        status=DatasetVersionStatus.PENDING_REVIEW,
    )

    approved = version.approve()

    assert version.status == DatasetVersionStatus.PENDING_REVIEW
    assert approved.status == DatasetVersionStatus.APPROVED
    assert approved.id == version.id
    assert approved.dataset_id == version.dataset_id

def test_pending_version_can_be_rejected_with_reason():
    version = DatasetVersion(
        id=uuid4(),
        dataset_id=uuid4(),
        status=DatasetVersionStatus.PENDING_REVIEW,
    )

    rejected = version.reject("Supplier submitted an invalid dataset")

    assert version.status == DatasetVersionStatus.PENDING_REVIEW
    assert rejected.status == DatasetVersionStatus.REJECTED
    assert rejected.rejection_reason == "Supplier submitted an invalid dataset"
    assert rejected.id == version.id
    assert rejected.dataset_id == version.dataset_id

def test_approved_version_cannot_be_approved_again():
    version = DatasetVersion(
        id=uuid4(),
        dataset_id=uuid4(),
        status=DatasetVersionStatus.APPROVED,
    )

    try:
        version.approve()
    except ValueError as error:
        assert str(error) == "Only pending versions can be approved"
    else:
        raise AssertionError("Expected ValueError")

def test_rejection_requires_a_reason():
    version = DatasetVersion(
        id=uuid4(),
        dataset_id=uuid4(),
        status=DatasetVersionStatus.PENDING_REVIEW,
    )

    try:
        version.reject("   ")
    except ValueError as error:
        assert str(error) == "Rejection reason is required"
    else:
        raise AssertionError("Expected ValueError")