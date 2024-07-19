# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

from typing import Dict, Optional

import requests

from hub_sdk.config import HUB_EXCEPTIONS
from hub_sdk.helpers.error_handler import ErrorHandler
from hub_sdk.helpers.logger import logger


class APIClientError(Exception):
    """
    Custom exception class for API client errors.

    This exception is raised when there is an error related to the API client, including HTTP errors and other client-side
    issues.

    Attributes:
        message (str): A human-readable error message.
        status_code (int | None): The HTTP status code associated with the error, if available.

    Methods:
        __str__: Returns a string representation of the APIClientError instance, which includes the error message.

    Example:
        ```python
        try:
            response = requests.get('https://api.example.com/data')
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise APIClientError('Failed to fetch data', status_code=e.response.status_code)
        ```

    References:
        - [Python Exceptions](https://docs.python.org/3/tutorial/errors.html)
        - [Requests Library](https://docs.python-requests.org/en/latest/)
    """

    def __init__(self, message: str, status_code: Optional[int] = None):
        """
        Initializes the APIClientError instance.

        Args:
            message (str): A human-readable error message.
            status_code (int | None): The HTTP status code associated with the error, if available.

        Returns:
            (None): This is an initializer and does not return a value.

        Example:
            ```python
            try:
                response = requests.get('https://example.com/api/resource')
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                raise APIClientError("Failed to fetch the resource", status_code=e.response.status_code)
            ```
        """
        super().__init__(message)
        self.status_code = status_code
        self.message = message

    def __str__(self) -> str:
        """
        Returns a string representation of the APIClientError instance.

        Returns:
            (str): The formatted error message, with the HTTP status code if available.

        Example:
            ```python
            try:
                raise APIClientError("Not Found", status_code=404)
            except APIClientError as e:
                print(str(e))  # "404: Not Found"
            ```
        """
        return f"{self.__class__.__name__}: {self.args[0]}"


class APIClient:
    """
    Represents an API client for making requests to a specified base URL.

    Attributes:
        base_url (str): The base URL for the API.
        headers (dict | None): Headers to be included in each request.
        logger (logging.Logger): An instance of the logger for logging purposes.

    Methods:
        get: Make a GET request to the API.
        post: Make a POST request to the API.
        put: Make a PUT request to the API.
        delete: Make a DELETE request to the API.
        patch: Make a PATCH request to the API.

    Example:
        ```python
        client = APIClient(base_url='https://api.example.com', headers={'Authorization': 'Bearer token'})
        response = client.get('/endpoint')
        if response:
            print(response.json())
        ```

    References:
        [Requests: HTTP for Humans](https://docs.python-requests.org/en/latest/)
    """

    def __init__(self, base_url: str, headers: Optional[Dict] = None):
        """
        Initializes an instance of the APIClient class.

        Args:
            base_url (str): The base URL for the API.
            headers (dict | None): Headers to be included in each request.

        Notes:
            This class is specifically designed for making HTTP requests to a given base URL. It supports
            custom headers which can be used for authorization or other purposes.
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
            data (dict | None): Form data to be sent in the request's body.
            json (dict | None): JSON data to be sent in the request's body.
            params (dict | None): Query parameters for the request.
            files (dict | None): Files to be sent as part of the form data.
            stream (bool): Whether to stream the response content (default is False).

        Returns:
            (Optional[requests.Response]): The response object from the HTTP request if successful; otherwise, None.

        Raises:
            APIClientError: If an error occurs during the request, with a message based on the HTTP status code.

        References:
            [requests library documentation](https://requests.readthedocs.io/en/latest/user/quickstart/)
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

        Example:
            ```python
            client = APIClient(base_url="https://api.example.com")
            response = client.get("/data", params={"key": "value"})
            ```

        References:
            - [requests library documentation](https://docs.python-requests.org/en/latest/): For more information on how to use the
              requests library.
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
            data (dict, optional): Data to be sent in the request's body.
            json (dict, optional): JSON data to be sent in the request's body.
            files (dict, optional): Files to be included in the request, if any.
            stream (bool, optional): If True, the response content will be streamed.

        Returns:
            (Optional[requests.Response]): The response object from the HTTP POST request, or None if it fails.

        Raises:
            (APIClientError): If an error occurs during the request, this exception is raised with an appropriate
            message based on the HTTP status code.

        Example:
            ```python
            client = APIClient(base_url="https://api.example.com", headers={"Authorization": "Bearer TOKEN"})
            response = client.post("/data", json={"key": "value"})
            if response:
                print(response.json())
            ```

        References:
            - [requests.post](https://docs.python-requests.org/en/master/user/quickstart/#make-a-request)
            - [Python requests streaming](https://requests.readthedocs.io/en/latest/user/advanced/#streaming-requests)
        """
        return self._make_request("POST", endpoint, data=data, json=json, files=files, stream=stream)

    def put(
        self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None
    ) -> Optional[requests.Response]:
        """
        Make a PUT request to the API.

        Args:
            endpoint (str): The endpoint to append to the base URL for the request.
            data (Optional[Dict], optional): Data to be sent in the request's body.
            json (Optional[Dict], optional): JSON data to be sent in the request's body.

        Returns:
            (Optional[requests.Response]): The response object from the HTTP PUT request.

        References:
            [Requests Library Documentation](https://docs.python-requests.org/en/latest/)
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

        References:
            [requests.request](https://docs.python-requests.org/en/master/api/#requests.request)
        """
        return self._make_request("DELETE", endpoint, params=params)

    def patch(
        self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None
    ) -> Optional[requests.Response]:
        """
        Make a PATCH request to the API.

        Args:
            endpoint (str): The endpoint to append to the base URL for the request.
            data (dict, optional): Data to be sent in the request's body.
            json (dict, optional): JSON data to be sent in the request's body.

        Returns:
            (Optional[requests.Response]): The response object from the HTTP PATCH request, or None if it fails.

        Example:
            ```python
            client = APIClient(base_url="https://api.example.com", headers={"Authorization": "Bearer token"})
            response = client.patch("/update/1", json={"key": "value"})
            if response:
                print(response.json())
            ```

        References:
            [requests documentation](https://docs.python-requests.org/en/latest/api/#requests.request)
        """
        return self._make_request("PATCH", endpoint, data=data, json=json)
