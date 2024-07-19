from tests.features.dataset import Dataset
from tests.features.model import Model
from tests.features.project import Project


class ObjectManager:
    """
    A class to manage interaction with datasets, models, and projects within a client context.

    Attributes:
        client (API_Client): The client instance used for making API requests and managing resources.

    Methods:
        get_model: Instantiates and returns a Model object using the current client instance.
        get_project: Instantiates and returns a Project object using the current client instance.
        get_dataset: Instantiates and returns a Dataset object using the current client instance.

    Example:
        ```python
        client = API_Client(api_key='your_api_key')
        manager = ObjectManager(client)

        model = manager.get_model()
        project = manager.get_project()
        dataset = manager.get_dataset()

        print(f"Model: {model}, Project: {project}, Dataset: {dataset}")
        ```

    References:
        [API documentation](https://example.com/api_docs) for more details on the client and its usage.
    """

    def __init__(self, client):
        """
        Initializes ObjectManager with a client for managing datasets, models, and projects.

        Args:
            client (any): The client instance used to interact with datasets, models, and projects.

        Example:
            ```python
            client_instance = SomeClient()
            object_manager = ObjectManager(client_instance)
            ```

        Notes:
            The client should support interfaces for datasets, models, and projects management.

        References:
            - [SomeClient Documentation](https://example.com/client-docs)
        """
        self.client = client

    def get_model(self):
        """
        Retrieves and initializes a Model object using the current client instance.

        Args:
            None

        Returns:
            Model: An instance of the Model class initialized with the current client.

        Example:
            ```python
            manager = ObjectManager(client)
            model_instance = manager.get_model()
            ```
        """
        return Model(self.client)

    def get_project(self):
        """
        Instantiates and returns a Project object using the current client instance.

        Args:
            None

        Returns:
            (Project): An instance of the Project class, initialized with the current client instance.

        Example:
            ```python
            object_manager = ObjectManager(client)
            project = object_manager.get_project()
            ```

        References:
            - [Python Google Style Guide](https://google.github.io/styleguide/pyguide.html)
            - [Python Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
        """
        return Project(self.client)

    def get_dataset(self):
        """
        Instantiates and returns a Dataset object using the current client instance.

        Args:
            None

        Returns:
            (Dataset): A Dataset object instantiated with the current client instance.

        Example:
            ```python
            object_manager = ObjectManager(client)
            dataset = object_manager.get_dataset()
            ```

        Notes:
            Ensure the client instance provided during ObjectManager initialization is valid and authorized to manage
            datasets.
        """
        return Dataset(self.client)
