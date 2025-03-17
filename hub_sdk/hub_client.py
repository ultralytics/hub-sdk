# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import os
from typing import Dict, Optional

from hub_sdk.base.auth import Auth
from hub_sdk.modules.datasets import DatasetList, Datasets
from hub_sdk.modules.models import ModelList, Models
from hub_sdk.modules.projects import ProjectList, Projects
from hub_sdk.modules.users import Users


def require_authentication(func) -> callable:
    """
    Ensure that the wrapped method can only be executed if the client is authenticated.

    Args:
        func (callable): The method to be wrapped.

    Returns:
        (callable): The wrapped method that checks authentication before execution.
    """

    def wrapper(self, *args, **kwargs):
        """Decorator to ensure a method is called only if the user is authenticated."""
        if not self.authenticated and not kwargs.get("public"):
            raise PermissionError("Access Denied: Authentication required.")
        return func(self, *args, **kwargs)

    return wrapper


class HUBClient(Auth):
    """
    A client class for interacting with a HUB service, extending authentication capabilities.

    Attributes:
        authenticated (bool): Indicates whether the client is authenticated.
        api_key (str): The API key for authentication.
        id_token (str): The identity token for authentication.
    """

    def __init__(self, credentials: Optional[Dict] = None):
        """
        Initialize the HUBClient instance.

        Args:
            credentials (Dict, optional): A dictionary containing authentication credentials.
                If None, the client will attempt to retrieve the API key from the environment variable "HUB_API_KEY".
        """
        super().__init__()
        self.authenticated = False
        if not credentials:
            self.api_key = os.environ.get("HUB_API_KEY")  # Safely retrieve the API key from an environment variable.
            credentials = {"api_key": self.api_key}

        self.login(**credentials)

    def login(self, api_key=None, id_token=None, email=None, password=None):
        """
        Log in the client using provided authentication credentials.

        Args:
            api_key (str, optional): The API key for authentication.
            id_token (str, optional): The identity token for authentication.
            email (str, optional): User's email.
            password (str, optional): User's password.
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

    def model(self, model_id: Optional[str] = None) -> Models:
        """
        Return an instance of the Models class for interacting with models.

        Args:
            model_id (str, optional): The identifier of the model. If provided, returns an instance associated with the
                specified model_id.

        Returns:
            (Models): An instance of the Models class.
        """
        return Models(model_id, self.get_auth_header())

    @require_authentication
    def dataset(self, dataset_id: str = None) -> Datasets:
        """
        Return an instance of the Datasets class for interacting with datasets.

        Args:
            dataset_id (str, optional): The identifier of the dataset. If provided, returns an instance associated with
                the specified dataset_id.

        Returns:
            (Datasets): An instance of the Datasets class.
        """
        return Datasets(dataset_id, self.get_auth_header())

    @require_authentication
    def team(self, arg):
        """Returns an instance of the Teams class for interacting with teams."""
        raise Exception("Coming Soon")

    @require_authentication
    def project(self, project_id: Optional[str] = None) -> Projects:
        """
        Return an instance of the Projects class for interacting with Projects.

        Args:
            project_id (str, optional): The identifier of the project. If provided, returns an instance associated with
                the specified project_id.

        Returns:
            (Projects): An instance of the Projects class.
        """
        return Projects(project_id, self.get_auth_header())

    @require_authentication
    def user(self, user_id: Optional[str] = None) -> Users:
        """
        Return an instance of the Users class for interacting with Projects.

        Args:
            user_id (str, optional): The identifier of the user. If provided, returns an instance associated with the
                specified user_id.

        Returns:
            (Users): An instance of the Users class.
        """
        return Users(user_id, self.get_auth_header())

    @require_authentication
    def model_list(self, page_size: Optional[int] = 10, public: Optional[bool] = None) -> ModelList:
        """
        Return a ModelList instance for interacting with a list of models.

        Args:
            page_size (int, optional): The number of models per page.
            public (bool, optional): Pass true to retrieve list of Public models list.

        Returns:
            (ModelList): An instance of the ModelList class.
        """
        return ModelList(page_size, public, self.get_auth_header())

    @require_authentication
    def project_list(self, page_size: Optional[int] = 10, public: Optional[bool] = None) -> ProjectList:
        """
        Return a ProjectList instance for interacting with a list of projects.

        Args:
            page_size (int, optional): The number of projects per page.
            public (bool, optional): Pass true to retrieve list of Public models list.

        Returns:
            (ProjectList): An instance of the ProjectList class.
        """
        return ProjectList(page_size, public, self.get_auth_header())

    @require_authentication
    def dataset_list(self, page_size: Optional[int] = 10, public: Optional[bool] = None) -> DatasetList:
        """
        Return a DatasetList instance for interacting with a list of datasets.

        Args:
            page_size (int, optional): The number of datasets per page.
            public (bool, optional): Pass true to retrieve list of Public dataset list.

        Returns:
            (DatasetList): An instance of the DatasetList class.
        """
        return DatasetList(page_size, public, self.get_auth_header())

    @require_authentication
    def team_list(self, page_size=None, public=None):
        """Fetches a list of team members with optional pagination."""
        raise Exception("Coming Soon")
