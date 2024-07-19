# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

import datetime
import http.client
from typing import Optional


class ErrorHandler:
    """
    Represents an error handler for managing HTTP status codes and error messages.

    This class provides methods to handle various HTTP errors by returning appropriate error messages based on the HTTP
    status code. It supports handling errors like unauthorized access, resource not found, internal server errors, and
    rate limit exceeded errors.

    Attributes:
        status_code (int): The HTTP status code associated with the error.
        message (Optional[str]): An optional error message providing additional details. Defaults to None.
        headers (Optional[dict]): An optional dictionary providing response headers details. Defaults to None.

    Methods:
        handle: Handles the error based on the provided status code and returns a descriptive error message.
        handle_unauthorized: Returns a message indicating unauthorized access (HTTP 401).
        handle_ratelimit_exceeded: Returns a message indicating rate limit exceeded (HTTP 429).
        handle_not_found: Returns a message indicating the resource was not found (HTTP 404).
        handle_internal_server_error: Returns a message indicating an internal server error (HTTP 500).
        handle_unknown_error: Returns a message indicating an unknown error occurred.
        get_default_message: Returns the default error message associated with the provided status code.

    Example:
        ```python
        error_handler = ErrorHandler(status_code=401)
        message = error_handler.handle()
        print(message)  # Outputs: "Unauthorized: Please check your credentials."
        ```

    References:
        - [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
    """

    def __init__(
        self,
        status_code: int,
        message: Optional[str] = None,
        headers: Optional[dict] = None,
    ):
        """
        Initializes the ErrorHandler object with a given status code, message, and optional headers.

        Args:
            status_code (int): The HTTP status code representing the error.
            message (Optional[str]): An optional error message providing additional details. Defaults to None.
            headers (Optional[dict]): An optional dictionary providing response headers details. Defaults to None.

        Returns:
            None

        Example:
            ```python
            error_handler = ErrorHandler(404, "Resource not found", {"Content-Type": "application/json"})
            ```

        Notes:
           - The headers attribute is typically used to provide additional context or metadata about the HTTP response.
        """
        self.status_code = status_code
        self.message = message
        self.headers = headers

    def handle(self) -> str:
        """
        Handles the error based on the provided HTTP status code.

        Returns:
            (str): A message describing the error.

        Example:
            ```python
            error_handler = ErrorHandler(status_code=404)
            error_message = error_handler.handle()
            ```
        """
        error_handlers = {
            401: self.handle_unauthorized,
            404: self.handle_not_found,
            500: self.handle_internal_server_error,
            429: self.handle_ratelimit_exceeded,
        }

        handler = error_handlers.get(self.status_code, self.get_default_message)
        return handler()

    @staticmethod
    def handle_unauthorized() -> str:
        """
        Handles an unauthorized error (HTTP 401).

        Returns:
            (str): An error message indicating unauthorized access.

        References:
            - [HTTP 401 Unauthorized](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401)

        Example:
            ```python
            error_handler = ErrorHandler(status_code=401)
            message = error_handler.handle()
            print(message)  # "Unauthorized access."
            ```
        """
        return "Unauthorized: Please check your credentials."

    def handle_ratelimit_exceeded(self) -> str:
        """
        Handles rate limit exceeded errors (HTTP 429).

        Args:
            None

        Returns:
            (str): An error message indicating rate limit exceeded. If "X-RateLimit-Reset" header is present, the
                message includes the reset time formatted as a datetime string.

        Notes:
            The function attempts to format the reset time from the "X-RateLimit-Reset" header, if available.
            If parsing fails, it defaults to "unknown".

        References:
            - [RFC 6585: Additional HTTP Status Codes](https://datatracker.ietf.org/doc/html/rfc6585)
        """
        error_msg = "Rate Limits Exceeded: Please try again later."

        if "X-RateLimit-Reset" in self.headers:
            rate_reset = self.headers.get("X-RateLimit-Reset")

            try:
                reset_time = datetime.datetime.fromtimestamp(int(rate_reset)).strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                reset_time = "unknown"

            error_msg = (
                "You have exceeded the rate limits for this request. "
                f"You will be able to make requests again after {reset_time}."
            )
        return error_msg

    @staticmethod
    def handle_not_found() -> str:
        """
        Handle a resource not found error (HTTP 404).

        Returns:
            (str): An error message indicating that the requested resource was not found.

        Example:
            ```python
            error_handler = ErrorHandler(status_code=404)
            message = error_handler.handle()
            print(message)  # Outputs: "Resource not found: The requested resource could not be located."
            ```

        References:
            - [HTTP 404 Error](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404)
        """
        return "Resource not found."

    @staticmethod
    def handle_internal_server_error() -> str:
        """
        Handles an internal server error (HTTP 500).

        Returns:
            (str): An error message indicating an internal server error.

        Notes:
            This error generally indicates that the server encountered an unexpected condition that prevented it from
            fulfilling the request. It is a generic error message and thus does not provide specific details about
            the cause of the failure.

        References:
            - [HTTP 500 Internal Server Error](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500)
        """
        return "Internal server error."

    @staticmethod
    def handle_unknown_error() -> str:
        """
        Handles an unknown error.

        Returns:
            (str): An error message indicating that an unknown error occurred.

        References:
            [HTTP Response Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
        """
        return "Unknown error occurred."

    def get_default_message(self) -> str:
        """
        Get the default error message for a given HTTP status code.

        Returns:
            (str): The default error message associated with the provided status code. If no specific message is
                found for the status code, the method falls back to handling an unknown error.

        References:
            - [HTTP status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
        """
        return http.client.responses.get(self.status_code, self.handle_unknown_error())
