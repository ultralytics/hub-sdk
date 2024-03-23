# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

from typing import Optional

import requests

from hub_sdk.config import FIREBASE_AUTH_URL, HUB_API_ROOT, HUB_WEB_ROOT, PREFIX
from hub_sdk.helpers.error_handler import ErrorHandler
from hub_sdk.helpers.logger import logger


class Auth:
    """
    Represents an authentication manager.

    Attributes:
        api_key (str, None): The API key used for authentication.
        id_token (str, None): The authentication token.
    """

    def __init__(self):
        """Initializes the Auth class with default authentication settings."""
        self.api_key = None
        self.id_token = None

    def authenticate(self) -> bool:
        """
        Attempt to authenticate with the server using either id_token or API key.

        Returns:
            (bool): True if authentication is successful, False otherwise.

        Raises:
            (ConnectionError): If request response is hasn't success in json, raised connection error exception.
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
            status_code = None
            if hasattr(e, "response"):
                status_code = e.response.status_code

            error_msg = ErrorHandler(status_code).handle()
            logger.warning(f"{PREFIX} {error_msg}")

        self.id_token = self.api_key = False  # reset invalid
        return False

    def get_auth_header(self) -> Optional[dict]:
        """
        Get the authentication header for making API requests.

        Returns:
            (Optional[dict]): The authentication header if id_token or API key is set, None otherwise.
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
        """
        return self.id_token or self.api_key

    def set_api_key(self, key: str):
        """
        Set the API key for authentication.

        Args:
            key (str): The API key string.
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
            status_code = None
            if hasattr(e, "response"):
                status_code = e.response.status_code

            error_msg = ErrorHandler(status_code).handle()
            logger.warning(f"{PREFIX} {error_msg}")
