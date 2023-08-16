import requests


class APIClientError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code

    def __str__(self):
        return f"{self.__class__.__name__}: {self.args[0]}"


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def _make_request(self, method, endpoint, data=None, params=None):
        url = self.base_url + endpoint
        try:
            response = requests.request(method, url, json=data, params=params)
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
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint, data=None):
        return self._make_request("POST", endpoint, data=data)

    def put(self, endpoint, data=None):
        return self._make_request("PUT", endpoint, data=data)

    def delete(self, endpoint):
        return self._make_request("DELETE", endpoint)
