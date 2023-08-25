import requests


class APIClientError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code

    def __str__(self):
        return f"{self.__class__.__name__}: {self.args[0]}"


class APIClient:
    def __init__(self, base_url, headers=None):
        """
        Initialize an instance of the APIClient class.

        Args:
            base_url (str): The base URL for the API.
            headers (dict, optional): Headers to be included in each request. Defaults to None.
        """
        self.base_url = base_url
        self.headers = headers

    def _make_request(self, method, endpoint, data=None, params=None):
        """
        Make an HTTP request to the API.

        Args:
            method (str): The HTTP method to use for the request (e.g., "GET", "POST").
            endpoint (str): The endpoint to append to the base URL for the request.
            data (dict, optional): Data to be sent in the request's body. Defaults to None.
            params (dict, optional): Query parameters for the request. Defaults to None.

        Returns:
            requests.Response: The response object from the HTTP request.

        Raises:
            APIClientError: If an error occurs during the request, this exception is raised with an appropriate message
                            based on the HTTP status code.
        """
        url = self.base_url + endpoint
        try:
            response = requests.request(method, url, json=data, params=params, headers=self.headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if response.status_code >= 400 and response.status_code < 500:
                raise APIClientError(
                    "Client error: Bad request or unauthorized.",
                    status_code=response.status_code,
                )
            elif response.status_code >= 500:
                raise APIClientError(
                    "Server error: Internal server error.",
                    status_code=response.status_code,
                )
            else:
                raise APIClientError(
                    "Unknown error occurred.", status_code=response.status_code
                )

    def get(self, endpoint, params=None):
        """
        Make a GET request to the API.

        Args:
            endpoint (str): The endpoint to append to the base URL for the request.
            params (dict, optional): Query parameters for the request. Defaults to None.

        Returns:
            requests.Response: The response object from the HTTP GET request.
        """
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint, data=None):
        """
        Make a POST request to the API.

        Args:
            endpoint (str): The endpoint to append to the base URL for the request.
            data (dict, optional): Data to be sent in the request's body. Defaults to None.

        Returns:
            requests.Response: The response object from the HTTP POST request.
        """
        return self._make_request("POST", endpoint, data=data)

    def put(self, endpoint, data=None):
        """
        Make a PUT request to the API.

        Args:
            endpoint (str): The endpoint to append to the base URL for the request.
            data (dict, optional): Data to be sent in the request's body. Defaults to None.

        Returns:
            requests.Response: The response object from the HTTP PUT request.
        """
        return self._make_request("PUT", endpoint, data=data)

    def delete(self, endpoint, params=None):
        """
        Make a DELETE request to the API.

        Args:
            endpoint (str): The endpoint to append to the base URL for the request.

        Returns:
            requests.Response: The response object from the HTTP DELETE request.
        """
        return self._make_request("DELETE", endpoint, params=params)
    
    def patch(self, endpoint, data=None):
        """
        Make a PATCH request to the API.

        Args:
            endpoint (str): The endpoint to append to the base URL for the request.
            data (dict, optional): Data to be sent in the request's body. Defaults to None.

        Returns:
            requests.Response: The response object from the HTTP PATCH request.
        """
        return self._make_request("PATCH", endpoint, data=data)
