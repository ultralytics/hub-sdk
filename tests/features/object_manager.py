from tests.features.dataset import Dataset
from tests.features.model import Model
from tests.features.project import Project


class ObjectManager:
    def __init__(self, client):
        self.client = client

    def get_model(self):
        return Model(self.client)

    def get_project(self):
        return Project(self.client)

    def get_dataset(self):
        return Dataset(self.client)
