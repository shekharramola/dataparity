from uuid import uuid4
from dataparity.domain.dataset import Dataset

dataset = Dataset(id=uuid4())

print(dataset)