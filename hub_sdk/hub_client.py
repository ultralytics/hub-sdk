import os

from hub_sdk.base.auth import Auth
from hub_sdk.modules.datasets import DatasetList, Datasets
from hub_sdk.modules.models import ModelList, Models
from hub_sdk.modules.projects import ProjectList, Projects
from hub_sdk.modules.users import Users


def require_authentication(func):
    """
    A decorator function to ensure that the wrapped method can only be executed if the client is authenticated.

    Args:
        func (callable): The method to be wrapped.

    Returns:
        callable: The wrapped method.
    """

    def wrapper(self, *args, **kwargs):
        if not self.authenticated and not kwargs.get("public"):
            raise PermissionError("Access Denied: Authentication required.")
        return func(self, *args, **kwargs)

    return wrapper


class HUBClient(Auth):
    """
    A client class for interacting with a HUB service, extending authentication capabilities.

    Args:
        credentials (dict): A dictionary containing authentication credentials.
                            Defaults to None. If None, the client will attempt
                            to retrieve the API key from the environment variable
                            "HUB_API_KEY".


    Attributes:
        authenticated (bool): Indicates whether the client is authenticated.
        api_key (str): The API key for authentication.
        id_token (str): The identity token for authentication.
    """

    def __init__(self, credentials=None):
        """
        Initializes the HUBClient instance.

        Args:
            credentials (dict): A dictionary containing authentication credentials.
        """
        self.authenticated = False
        if not credentials:
            self.api_key = os.environ.get("HUB_API_KEY")  # Safely retrieve the API key from an environment variable.
            credentials = {"api_key": self.api_key}

        self.login(**credentials)

    def login(self, api_key=None, id_token=None, email=None, password=None):
        """
        Logs in the client using provided authentication credentials.

        Args:
            api_key (str): The API key for authentication.
            id_token (str): The identity token for authentication.
            email (str): User's email.
            password (str): User's password.
        """
        self.api_key = api_key
        self.id_token = id_token
        if self.api_key or self.id_token:
            if self.authenticate():
                self.authenticated = True

        elif email and password:
            if self.authorize(email, password):
                self.authenticated = True

    @require_authentication
    def model(self, model_id: str = None):
        """
        Returns an instance of the Models class for interacting with models.

        Returns:
            Models: An instance of the Models class.
        """
        return Models(model_id, self.get_auth_header())

    @require_authentication
    def dataset(self, dataset_id: str = None):
        """
        Returns an instance of the Datasets class for interacting with datasets.

        Returns:
            Datasets: An instance of the Datasets class.
        """
        raise Exception("Coming Soon")

    @require_authentication
    def team(self, arg):
        raise Exception("Coming Soon")

    @require_authentication
    def project(self, project_id: str = None):
        """
        Returns an instance of the Projects class for interacting with Projects.

        Returns:
            Projects: An instance of the Projects class.
        """
        raise Exception("Coming Soon")

    @require_authentication
    def user(self, user_id: str = None):
        """
        Returns an instance of the Projects class for interacting with Projects.

        Returns:
            Projects: An instance of the Projects class.
        """
        return Users(user_id, self.get_auth_header())

    @require_authentication
    def model_list(self, page_size: int = None, public: bool = None):
        """
        Returns a ModelList instance for interacting with a list of models.

        Args:
            page_size (int, optional): The number of models per page. Defaults to None.
            public (bool, optional):

        Returns:
            ModelList: An instance of the ModelList class.
        """
        return ModelList(page_size, public, self.get_auth_header())

    @require_authentication
    def project_list(self, page_size: int = None, public: bool = None):
        """
        Returns a ProjectList instance for interacting with a list of projects.

        Args:
            page_size (int, optional): The number of projects per page. Defaults to None.

        Returns:
            ProjectList: An instance of the ProjectList class.
        """
        raise Exception("Coming Soon")

    @require_authentication
    def dataset_list(self, page_size: int = None, public: bool = None):
        """
        Returns a DatasetList instance for interacting with a list of datasets.

        Args:
            page_size (int, optional): The number of datasets per page. Defaults to None.

        Returns:
            DatasetList: An instance of the DatasetList class.
        """
        raise Exception("Coming Soon")

    @require_authentication
    def team_list(self, page_size=None, public=None):
        raise Exception("Coming Soon")
