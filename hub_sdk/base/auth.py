# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from typing import Optional

import requests

from hub_sdk.config import FIREBASE_AUTH_URL, HUB_API_ROOT, HUB_WEB_ROOT, PREFIX
from hub_sdk.helpers.error_handler import ErrorHandler
from hub_sdk.helpers.logger import logger


class Auth:
    """
    Represents an authentication manager for Ultralytics Hub API.

    This class handles authentication using either an API key or ID token, providing methods to authenticate, authorize,
    and manage authentication state.

    Attributes:
        api_key (str | None): The API key used for authentication with the Hub API.
        id_token (str | None): The authentication token received after successful authorization.

    Methods:
        authenticate: Attempt to authenticate with the server using either id_token or API key.
        get_auth_header: Get the authentication header for making API requests.
        get_state: Get the authentication state.
        set_api_key: Set the API key for authentication.
        authorize: Authorize the user by obtaining an idToken through email and password.
    """

    def __init__(self):
        """Initialize the Auth class with default authentication settings."""
        self.api_key = None
        self.id_token = None

    def authenticate(self) -> bool:
        """
        Attempt to authenticate with the server using either id_token or API key.

        Makes a POST request to the authentication endpoint with the appropriate authentication header.
        Handles connection errors and request exceptions.

        Returns:
            (bool): True if authentication is successful, False otherwise.

        Raises:
            ConnectionError: If authentication fails or user has not authenticated locally.
        """
        try:
            if header := self.get_auth_header():
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

        self.id_token = self.api_key = False  # reset invalid credentials
        return False

    def get_auth_header(self) -> Optional[dict]:
        """
        Get the authentication header for making API requests.

        Creates the appropriate header based on whether an ID token or API key is available.

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
        return bool(self.id_token or self.api_key)

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

        Makes a request to the Firebase authentication URL with the provided credentials.
        Handles connection errors and request exceptions.

        Args:
            email (str): User's email address.
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
            status_code = e.response.status_code if hasattr(e, "response") else None
            error_msg = ErrorHandler(status_code).handle()
            logger.warning(f"{PREFIX} {error_msg}")
        return False
