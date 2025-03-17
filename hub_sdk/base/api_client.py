# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from typing import Dict, Optional

import requests

from hub_sdk.config import HUB_EXCEPTIONS
from hub_sdk.helpers.error_handler import ErrorHandler
from hub_sdk.helpers.logger import logger


class APIClientError(Exception):
    """
    Custom exception class for API client errors.

    Attributes:
        message (str): A human-readable error message.
        status_code (int, optional): The HTTP status code associated with the error, if available.
    """

    def __init__(self, message: str, status_code: Optional[int] = None):
        """
        Initialize the APIClientError instance.

        Args:
            message (str): A human-readable error message.
            status_code (int, optional): The HTTP status code associated with the error.
        """
        super().__init__(message)
        self.status_code = status_code
        self.message = message

    def __str__(self) -> str:
        """Return a string representation of the APIClientError instance."""
        return f"{self.__class__.__name__}: {self.args[0]}"


class APIClient:
    """
    Represents an API client for making requests to a specified base URL.

    Attributes:
        base_url (str): The base URL for the API.
        headers (Dict, optional): Headers to be included in each request.
        logger (logging.Logger): An instance of the logger for logging purposes.
    """

    def __init__(self, base_url: str, headers: Optional[Dict] = None):
        """
        Initialize an instance of the APIClient class.

        Args:
            base_url (str): The base URL for the API.
            headers (Dict, optional): Headers to be included in each request.
        """
        self.base_url = base_url
        self.headers = headers
        self.logger = logger

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        json: Optional[Dict] = None,
        params: Optional[Dict] = None,
        files: Optional[Dict] = None,
        stream: bool = False,
    ) -> Optional[requests.Response]:
        """
        Make an HTTP request to the API.

        Args:
            method (str): The HTTP method to use for the request (e.g., "GET", "POST").
            endpoint (str): The endpoint to append to the base URL for the request.
            data (Dict, optional): Data to be sent in the request's body.
            json (Dict, optional): JSON data to be sent in the request's body.
            params (Dict, optional): Query parameters for the request.
            files (Dict, optional): Files to be sent as part of the form data.
            stream (bool): Whether to stream the response content.

        Returns:
            (Optional[requests.Response]): The response object from the HTTP request, None if it fails and
                HUB_EXCEPTIONS is off.

        Raises:
            APIClientError: If an error occurs during the request, this exception is raised with an appropriate
                message based on the HTTP status code.
        """
        # Overwrite the base url if a http url is submitted
        url = endpoint if endpoint.startswith("http") else self.base_url + endpoint

        kwargs = {"params": params, "files": files, "headers": self.headers, "stream": stream}

        # Determine the request data based on 'data' or 'json_data'
        if json is not None:
            kwargs["json"] = json
        else:
            kwargs["data"] = data

        try:
            response = requests.request(method, url, **kwargs)

            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            status_code = None
            # To handle Timeout and ConnectionError exceptions
            if hasattr(e, "response") and e.response is not None:
                status_code = e.response.status_code

            error_msg = ErrorHandler(status_code, headers=response.headers).handle()
            self.logger.error(error_msg)

            if not HUB_EXCEPTIONS:
                raise APIClientError(error_msg, status_code=status_code) from e

    def get(self, endpoint: str, params=None) -> Optional[requests.Response]:
        """
        Make a GET request to the API.

        Args:
            endpoint (str): The endpoint to append to the base URL for the request.
            params (dict, optional): Query parameters for the request.

        Returns:
            (Optional[requests.Response]): The response object from the HTTP GET request, None if it fails.
        """
        return self._make_request("GET", endpoint, params=params)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        json: Optional[Dict] = None,
        files: Optional[Dict] = None,
        stream=False,
    ) -> Optional[requests.Response]:
        """
        Make a POST request to the API.

        Args:
            endpoint (str): The endpoint to append to the base URL for the request.
            data (Dict, optional): Data to be sent in the request's body.
            json (Dict, optional): JSON data to be sent in the request's body.
            files (Dict, optional): Files to be included in the request.
            stream (bool): If True, the response content will be streamed.

        Returns:
            (Optional[requests.Response]): The response object from the HTTP POST request.
        """
        return self._make_request("POST", endpoint, data=data, json=json, files=files, stream=stream)

    def put(
        self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None
    ) -> Optional[requests.Response]:
        """
        Make a PUT request to the API.

        Args:
            endpoint (str): The endpoint to append to the base URL for the request.
            data (Dict, optional): Data to be sent in the request's body.
            json (Dict, optional): JSON data to be sent in the request's body.

        Returns:
            (Optional[requests.Response]): The response object from the HTTP PUT request.
        """
        return self._make_request("PUT", endpoint, data=data, json=json)

    def delete(self, endpoint: str, params: Optional[Dict] = None) -> Optional[requests.Response]:
        """
        Make a DELETE request to the API.

        Args:
            endpoint (str): The endpoint to append to the base URL for the request.
            params (dict, optional): Parameters to include in the request.

        Returns:
            (Optional[requests.Response]): The response object from the HTTP DELETE request, or None if it fails.
        """
        return self._make_request("DELETE", endpoint, params=params)

    def patch(
        self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None
    ) -> Optional[requests.Response]:
        """
        Make a PATCH request to the API.

        Args:
            endpoint (str): The endpoint to append to the base URL for the request.
            data (Dict, optional): Data to be sent in the request's body.
            json (Dict, optional): JSON data to be sent in the request's body.

        Returns:
            (Optional[requests.Response]): The response object from the HTTP PATCH request.
        """
        return self._make_request("PATCH", endpoint, data=data, json=json)
