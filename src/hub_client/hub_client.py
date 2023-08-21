from .auth import Auth
from .models import Models
from .datasets import Datasets
import os

def require_authentication(func):
    """
    A decorator function to ensure that the wrapped method can only be executed
    if the client is authenticated.

    Args:
        func (callable): The method to be wrapped.

    Returns:
        callable: The wrapped method.
    """
    def wrapper(self, *args, **kwargs):
        if not self.authenticated:
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
            self.authenticated = True

        elif email and password:
            if self.authorize(email, password):
                self.authenticated = True  


    @require_authentication
    def models(self):
        """
        Returns an instance of the Models class for interacting with models.

        Returns:
            Models: An instance of the Models class.
        """
        return Models(self.get_auth_header())

    @require_authentication
    def datasets(self):
        """
        Returns an instance of the Datasets class for interacting with datasets.

        Returns:
            Datasets: An instance of the Datasets class.
        """
        return Datasets(self.get_auth_header())
