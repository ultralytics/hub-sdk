# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

import os
from typing import Dict, Optional

from hub_sdk.base.auth import Auth
from hub_sdk.modules.datasets import DatasetList, Datasets
from hub_sdk.modules.models import ModelList, Models
from hub_sdk.modules.projects import ProjectList, Projects
from hub_sdk.modules.users import Users


def require_authentication(func) -> callable:
    """
    A decorator function to ensure that the wrapped method can only be executed if the client is authenticated.

    Args:
        func (callable): The method to be wrapped.

    Returns:
        (callable): The wrapped method with additional authentication check.

    Example:
        ```python
        class SomeClass:
            def __init__(self, authenticated):
                self.authenticated = authenticated

            @require_authentication
            def some_method(self):
                print("This method is authenticated.")

        instance = SomeClass(authenticated=True)
        instance.some_method()  # This will print the message
        ```

        ```python
        instance = SomeClass(authenticated=False)
        try:
            instance.some_method()  # This will raise PermissionError
        except PermissionError as e:
            print(e)  # Output: Access Denied: Authentication required.
        ```

    Notes:
        The decorator checks the `self.authenticated` attribute of the class instance and raises a
        `PermissionError` if the client is not authenticated and the 'public' keyword argument is not set to True.

    References:
        [Python Decorators](https://realpython.com/primer-on-python-decorators/)
    """

    def wrapper(self, *args, **kwargs):
        """Decorator to ensure a method is called only if the user is authenticated."""
        if not self.authenticated and not kwargs.get("public"):
            raise PermissionError("Access Denied: Authentication required.")
        return func(self, *args, **kwargs)

    return wrapper


class HUBClient(Auth):
    """
    A client class for interacting with a HUB service, providing access to models, datasets, projects, and users.

    The HUBClient class extends authentication capabilities from the Auth base class and offers methods
    for managing and retrieving various resources from a HUB service.

    Attributes:
        authenticated (bool): Indicates whether the client is authenticated.
        api_key (str): The API key for authentication.
        id_token (str): The identity token for authentication.

    Methods:
        login: Logs in the client using provided authentication credentials.
        model: Returns an instance of the Models class for interacting with models.
        dataset: Returns an instance of the Datasets class for interacting with datasets.
        team: Placeholder method for interacting with teams (not yet implemented).
        project: Returns an instance of the Projects class for interacting with projects.
        user: Returns an instance of the Users class for interacting with users.
        model_list: Returns a ModelList instance for interacting with a list of models.
        project_list: Returns a ProjectList instance for interacting with a list of projects.
        dataset_list: Returns a DatasetList instance for interacting with a list of datasets.
        team_list: Fetches a list of team members with optional pagination (not yet implemented).

    Example:
        ```python
        client = HUBClient(credentials={'api_key': 'your_api_key'})
        if client.authenticated:
            models = client.model_list()
            for model in models:
                print(model)
        ```

    References:
        - [Ultralytics GitHub Repository](https://github.com/ultralytics/ultralytics)
        - [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
    """

    def __init__(self, credentials: Optional[Dict] = None):
        """
        Initializes the HUBClient instance.

        Args:
            credentials (dict | None): A dictionary containing authentication credentials. If None, the client
                will attempt to retrieve the API key from the environment variable "HUB_API_KEY".

        Returns:
            None

        Notes:
            The `credentials` dictionary should ideally contain keys like 'api_key' or 'id_token' needed for authentication.

        References:
            [Hub SDK Authentication](https://github.com/ultralytics/hub-sdk)
        """
        super().__init__()
        self.authenticated = False
        if not credentials:
            self.api_key = os.environ.get("HUB_API_KEY")  # Safely retrieve the API key from an environment variable.
            credentials = {"api_key": self.api_key}

        self.login(**credentials)

    def login(self, api_key=None, id_token=None, email=None, password=None):
        """
        Logs in the client using provided authentication credentials.

        Args:
            api_key (str, optional): The API key for authentication.
            id_token (str, optional): The identity token for authentication.
            email (str, optional): User's email address.
            password (str, optional): User's password.

        Returns:
            (bool): True if successfully authenticated, False otherwise.

        Notes:
            The method prioritizes API key or identity token authentication. If neither of these are provided,
            it falls back to email and password-based authorization.

        Example:
            ```python
            client = HUBClient()
            success = client.login(api_key='your_api_key')
            if success:
                print("Logged in successfully.")
            ```

        References:
            - [Python Decorators](https://docs.python.org/3/glossary.html#term-decorator)
            - [API Key Management](https://en.wikipedia.org/wiki/Application_programming_interface_key)
            - [User Authentication](https://en.wikipedia.org/wiki/Authentication)
        """
        self.api_key = api_key
        self.id_token = id_token
        if (
            (self.api_key or self.id_token)
            and self.authenticate()
            or not self.api_key
            and not self.id_token
            and email
            and password
            and self.authorize(email, password)
        ):
            self.authenticated = True

    @require_authentication
    def model(self, model_id: Optional[str] = None) -> Models:
        """
        Returns an instance of the Models class for interacting with models.

        Args:
            model_id (str, optional): The identifier of the model. If provided, returns an instance associated with the
                specified model_id.

        Returns:
            (Models): An instance of the Models class.

        Example:
            ```python
            client = HUBClient(credentials={"api_key": "your_api_key"})
            model_instance = client.model(model_id="your_model_id")
            ```

        Notes:
            This function requires authentication.
        """
        return Models(model_id, self.get_auth_header())

    @require_authentication
    def dataset(self, dataset_id: str = None) -> Datasets:
        """
        Returns an instance of the Datasets class for interacting with datasets.

        Args:
            dataset_id (str, optional): The identifier of the dataset. If provided, returns an instance associated
                with the specified dataset_id.

        Returns:
            (Datasets): An instance of the Datasets class for managing dataset operations.

        Example:
            ```python
            client = HUBClient({"api_key": "your_api_key"})
            dataset_instance = client.dataset("dataset_id")
            ```

        Notes:
            Ensure that the client is authenticated before attempting to retrieve a dataset instance.

        References:
            [Ultralytics HUB SDK Documentation](https://github.com/ultralytics/hub-sdk)
        """
        return Datasets(dataset_id, self.get_auth_header())

    @require_authentication
    def team(self, arg):
        """
        Returns an instance of the Teams class for interacting with teams.

        Args:
            arg (str): An argument affecting the operation on the Teams class.

        Returns:
            (Teams): An instance of the Teams class.
        """
        raise Exception("Coming Soon")

    @require_authentication
    def project(self, project_id: Optional[str] = None) -> Projects:
        """
        Returns an instance of the Projects class for interacting with Projects.

        Args:
            project_id (str, optional): The identifier of the project. If provided, returns an instance associated
                with the specified project_id.

        Returns:
            (Projects): An instance of the Projects class.

        Example:
            ```python
            hub_client = HUBClient(credentials={"api_key": "YOUR_API_KEY"})
            project_instance = hub_client.project(project_id="12345")
            ```
        """
        return Projects(project_id, self.get_auth_header())

    @require_authentication
    def user(self, user_id: Optional[str] = None) -> Users:
        """
        Returns an instance of the Users class for interacting with users.

        Args:
            user_id (str, optional): The identifier of the user. If provided, returns an instance associated with
                the specified user_id.

        Returns:
            (Users): An instance of the Users class.

        Example:
            ```python
            client = HUBClient(credentials={'api_key': 'your_api_key'})
            user_instance = client.user(user_id='12345')
            ```
        """
        return Users(user_id, self.get_auth_header())

    @require_authentication
    def model_list(self, page_size: Optional[int] = 10, public: Optional[bool] = None) -> ModelList:
        """
        Returns a ModelList instance for interacting with a list of models.

        Args:
            page_size (int, optional): The number of models per page. Defaults to 10.
            public (bool, optional): Pass True to retrieve the list of public models. Defaults to None.

        Returns:
            (ModelList): An instance of the ModelList class.

        Example:
            ```python
            client = HUBClient(credentials={"api_key": "your_api_key"})
            model_list = client.model_list(page_size=20, public=True)
            ```
        """
        return ModelList(page_size, public, self.get_auth_header())

    @require_authentication
    def project_list(self, page_size: Optional[int] = 10, public: Optional[bool] = None) -> ProjectList:
        """
        Returns a ProjectList instance for interacting with a list of projects.

        Args:
            page_size (int, optional): The number of projects per page.
            public (bool, optional): Pass true to retrieve the list of public projects.

        Returns:
            (ProjectList): An instance of the ProjectList class.

        Example:
            ```python
            client = HUBClient({"api_key": "your_api_key"})
            projects = client.project_list(page_size=5, public=True)
            ```
        """
        return ProjectList(page_size, public, self.get_auth_header())

    @require_authentication
    def dataset_list(self, page_size: Optional[int] = 10, public: Optional[bool] = None) -> DatasetList:
        """
        Returns a DatasetList instance for interacting with a list of datasets.

        Args:
            page_size (int, optional): The number of datasets per page.
            public (bool, optional): Pass true to retrieve a list of public datasets.

        Returns:
            (DatasetList): An instance of the DatasetList class.

        Example:
            ```python
            client = HUBClient(credentials={"api_key": "your_api_key"})
            datasets = client.dataset_list(page_size=20, public=True)
            ```
        """
        return DatasetList(page_size, public, self.get_auth_header())

    @require_authentication
    def team_list(self, page_size=None, public=None):
        """
        Fetches a list of team members with optional pagination.

        Args:
            page_size (int | None): The number of team members to retrieve per page. If None, a default value is used.
            public (bool | None): Whether to retrieve public team members only. If None, retrieves team members based
                on authentication context.

        Returns:
            (list[dict]): A list of dictionaries, each representing a team member's details.

        References:
            [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

        Example:
            ```python
            client = HUBClient(credentials={"api_key": "your_api_key"})
            team_members = client.team_list(page_size=20, public=True)
            ```
        """
        raise Exception("Coming Soon")
