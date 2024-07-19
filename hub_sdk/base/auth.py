# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

from typing import Optional

import requests

from hub_sdk.config import FIREBASE_AUTH_URL, HUB_API_ROOT, HUB_WEB_ROOT, PREFIX
from hub_sdk.helpers.error_handler import ErrorHandler
from hub_sdk.helpers.logger import logger


class Auth:
    """
    Represents an authentication manager.

    Manages API key and ID token-based authentication, enabling the authorization of users and managing
    authenticated sessions.

    Attributes:
        api_key (str | None): The API key used for authentication.
        id_token (str | None): The authentication token.

    Methods:
        authenticate: Attempt to authenticate with the server using either id_token or API key.
        get_auth_header: Get the authentication header for making API requests.
        get_state: Get the authentication state.
        set_api_key: Set the API key for authentication.
        authorize: Authorize the user by obtaining an ID token through a POST request with email and password.

    Example:
        ```python
        auth = Auth()
        auth.set_api_key('your_api_key')
        if auth.authenticate():
            print("Authenticated successfully")
        else:
            print("Authentication failed")
        ```

    References:
        - [Firebase Auth REST API](https://firebase.google.com/docs/reference/rest/auth)
        - [Requests: HTTP for Humans](https://docs.python-requests.org/en/master/)
    """

    def __init__(self):
        """
        Initializes the Auth class with default authentication settings.

        Args:
            None

        Returns:
            None

        Notes:
            This constructor sets the initial state of the Auth instance, with `api_key` and `id_token`
            attributes set to None.

        References:
            [Requests Library](https://docs.python-requests.org/en/latest/)
        """
        self.api_key = None
        self.id_token = None

    def authenticate(self) -> bool:
        """
        Attempt to authenticate with the server using either id_token or API key.

        Returns:
            (bool): True if authentication is successful, False otherwise.

        Raises:
            (ConnectionError): If request response fails, raises a connection error exception.

        Example:
            ```python
            auth = Auth()
            auth.api_key = "your_api_key"
            success = auth.authenticate()
            if success:
                print("Authenticated successfully!")
            else:
                print("Authentication failed.")
            ```
        """
        try:
            header = self.get_auth_header()
            if header:
                r = requests.post(f"{HUB_API_ROOT}/v1/auth", headers=header)
                if not r.json().get("success", False):
                    raise ConnectionError("Unable to authenticate.")
                return True
            raise ConnectionError("User has not authenticated locally.")
        except ConnectionError:
            logger.warning(f"{PREFIX} Invalid API key ⚠️")
        except requests.exceptions.RequestException as e:
            status_code = e.response.status_code if hasattr(e, "response") else None
            error_msg = ErrorHandler(status_code).handle()
            logger.warning(f"{PREFIX} {error_msg}")

        self.id_token = self.api_key = False  # reset invalid
        return False

    def get_auth_header(self) -> Optional[dict]:
        """
        Get the authentication header for making API requests.

        Returns:
            (Optional[dict]): The authentication header if id_token or API key is set, None otherwise.

        Example:
            ```python
            auth = Auth()
            auth.id_token = 'your_id_token'
            header = auth.get_auth_header()
            ```

        References:
            - [requests library](https://docs.python-requests.org/en/master/)
            - [Firebase Auth REST API](https://firebase.google.com/docs/reference/rest/auth)
        """
        if self.id_token:
            return {"authorization": f"Bearer {self.id_token}"}
        elif self.api_key:
            return {"x-api-key": self.api_key}
        else:
            return None

    def get_state(self) -> bool:
        """
        Get the authentication state.

        Returns:
            (bool): True if either id_token or API key is set, False otherwise.

        Example:
            ```python
            auth = Auth()
            is_authenticated = auth.get_state()
            ```
        """
        return self.id_token or self.api_key

    def set_api_key(self, key: str):
        """
        Sets the API key for authentication.

        Args:
            key (str): The API key string to be used for authentication.

        Returns:
            None

        Notes:
            This method does not validate the API key; it merely stores it for future authentication requests.
        """
        self.api_key = key

    def authorize(self, email: str, password: str) -> bool:
        """
        Authorize the user by obtaining an idToken through a POST request with email and password.

        Args:
            email (str): User's email.
            password (str): User's password.

        Returns:
            (bool): True if authorization is successful, False otherwise.

        Notes:
            This function uses the Firebase Authentication service to verify user credentials.

        References:
            [Firebase Authentication](https://firebase.google.com/docs/auth)
            [requests Library](https://docs.python-requests.org/en/latest/)
        """
        try:
            headers = {"origin": HUB_WEB_ROOT}
            response = requests.post(FIREBASE_AUTH_URL, json={"email": email, "password": password}, headers=headers)
            if response.status_code == 200:
                self.id_token = response.json().get("idToken")
                return True
            else:
                raise ConnectionError("Authorization failed.")
        except ConnectionError:
            logger.warning(f"{PREFIX} Invalid API key ⚠️")
        except requests.exceptions.RequestException as e:
            status_code = e.response.status_code if hasattr(e, "response") else None
            error_msg = ErrorHandler(status_code).handle()
            logger.warning(f"{PREFIX} {error_msg}")
