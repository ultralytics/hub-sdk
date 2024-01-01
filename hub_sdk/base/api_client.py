import requests

from hub_sdk.config import HUB_EXCEPTIONS
from hub_sdk.helpers.error_handler import ErrorHandler
from hub_sdk.helpers.logger import logger


class APIClientError(Exception):
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.args[0]}"


class APIClient:
    def __init__(self, base_url: str, headers: dict = None):
        """
        Initialize an instance of the APIClient class.

        Args:
            base_url (str): The base URL for the API.
            headers (dict, optional): Headers to be included in each request. Defaults to None.
        """
        self.base_url = base_url
        self.headers = headers
        self.logger = logger

    def _make_request(
        self, method: str, endpoint: str, data: dict = None, json=None, params=None, files=None, stream: bool = False
    ):
        """
        Make an HTTP request to the API.

        Args:
            method (str): The HTTP method to use for the request (e.g., "GET", "POST").
            endpoint (str): The endpoint to append to the base URL for the request.
            data (dict, optional): Data to be sent in the request's body. Defaults to None.
            json_data (dict, optional): JSON data to be sent in the request's body. Defaults to None.
            params (dict, optional): Query parameters for the request. Defaults to None.
            files (dict, optional): Files to be sent as part of the form data. Defaults to None.
            stream (bool, optional): Whether to stream the response content. Defaults to False.

        Returns:
            requests.Response: The response object from the HTTP request.

        Raises:
            APIClientError: If an error occurs during the request, this exception is raised with an appropriate message
                            based on the HTTP status code.
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
            error_msg = ErrorHandler(e.response.status_code).handle()
            self.logger.error(error_msg)

            if not HUB_EXCEPTIONS:
                raise APIClientError(
                    error_msg,
                    status_code=response.status_code,
                )

    def get(self, endpoint: str, params=None):
        """
        Make a GET request to the API.

        Args:
            endpoint (str): The endpoint to append to the base URL for the request.
            params (dict, optional): Query parameters for the request. Defaults to None.

        Returns:
            requests.Response: The response object from the HTTP GET request.
        """
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: dict = None, json=None, files=None):
        """
        Make a POST request to the API.

        Args:
            endpoint (str): The endpoint to append to the base URL for the request.
            data (dict, optional): Data to be sent in the request's body. Defaults to None.

        Returns:
            requests.Response: The response object from the HTTP POST request.
        """
        return self._make_request("POST", endpoint, data=data, json=json, files=files)

    def put(self, endpoint: str, data=None, json=None):
        """
        Make a PUT request to the API.

        Args:
            endpoint (str): The endpoint to append to the base URL for the request.
            data (dict, optional): Data to be sent in the request's body. Defaults to None.

        Returns:
            requests.Response: The response object from the HTTP PUT request.
        """
        return self._make_request("PUT", endpoint, data=data, json=json)

    def delete(self, endpoint: str, params=None):
        """
        Make a DELETE request to the API.

        Args:
            endpoint (str): The endpoint to append to the base URL for the request.

        Returns:
            requests.Response: The response object from the HTTP DELETE request.
        """
        return self._make_request("DELETE", endpoint, params=params)

    def patch(self, endpoint: str, data=None, json=None):
        """
        Make a PATCH request to the API.

        Args:
            endpoint (str): The endpoint to append to the base URL for the request.
            data (dict, optional): Data to be sent in the request's body. Defaults to None.

        Returns:
            requests.Response: The response object from the HTTP PATCH request.
        """
        return self._make_request("PATCH", endpoint, data=data, json=json)
