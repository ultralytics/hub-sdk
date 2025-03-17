# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from tests.features.dataset import Dataset
from tests.features.model import Model
from tests.features.project import Project


class ObjectManager:
    """
    Manages instantiation and retrieval of dataset, model, and project objects using a client instance.

    This class provides a centralized way to create and access Dataset, Model, and Project objects
    with a shared client instance.

    Attributes:
        client (Any): The client instance used for API communication when creating objects.

    Methods:
        get_model: Creates and returns a Model object with the current client.
        get_project: Creates and returns a Project object with the current client.
        get_dataset: Creates and returns a Dataset object with the current client.
    """

    def __init__(self, client):
        """Initialize the ObjectManager with a client instance for API communication."""
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
