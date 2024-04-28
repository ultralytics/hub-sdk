from tests.features.dataset import Dataset
from tests.features.model import Model
from tests.features.project import Project


class ObjectManager:
    def __init__(self, client):
        """Initializes ObjectManager with a client for managing datasets, models, and projects."""
        self.client = client

    def get_model(self):
        """Instantiates and returns a Model object using the current client instance."""
        return Model(self.client)

    def get_project(self):
        """Instantiates and returns a Project object using the current client instance."""
        return Project(self.client)

    def get_dataset(self):
        """Instantiates and returns a Dataset object using the current client instance."""
        return Dataset(self.client)
