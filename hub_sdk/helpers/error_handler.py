# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import datetime
import http.client
from typing import Optional


class ErrorHandler:
    """
    Represents an error handler for managing HTTP status codes and error messages.

    Attributes:
        status_code (int): The HTTP status code associated with the error.
        message (str | None): An optional error message providing additional details.
        headers (dict | None): An optional dictionary providing response headers details.

    Methods:
        handle: Handle the error based on the provided status code.
        handle_unauthorized: Handle an unauthorized error (HTTP 401).
        handle_ratelimit_exceeded: Handle rate limit exceeded error (HTTP 429).
        handle_not_found: Handle a resource not found error (HTTP 404).
        handle_internal_server_error: Handle an internal server error (HTTP 500).
        handle_unknown_error: Handle an unknown error.
        get_default_message: Get the default error message for a given HTTP status code.
    """

    def __init__(
        self,
        status_code: int,
        message: Optional[str] = None,
        headers: Optional[dict] = None,
    ):
        """
        Initialize the ErrorHandler object with a given status code.

        Args:
            status_code (int): The HTTP status code representing the error.
            message (str, optional): An optional error message providing additional details.
            headers (dict, optional): An optional dictionary providing response headers details.
        """
        self.status_code = status_code
        self.message = message
        self.headers = headers

    def handle(self) -> str:
        """
        Handle the error based on the provided status code.

        Returns:
            (str): A message describing the error.
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
        Handle an unauthorized error (HTTP 401).

        Returns:
            (str): An error message indicating unauthorized access.
        """
        return "Unauthorized: Please check your credentials."

    def handle_ratelimit_exceeded(self) -> str:
        """
        Handle rate limit exceeded error (HTTP 429).

        Returns:
            (str): An error message indicating rate limit exceeded with reset time if available.
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
        """
        return "Resource not found."

    @staticmethod
    def handle_internal_server_error() -> str:
        """
        Handle an internal server error (HTTP 500).

        Returns:
            (str): An error message indicating an internal server error.
        """
        return "Internal server error."

    @staticmethod
    def handle_unknown_error() -> str:
        """
        Handle an unknown error.

        Returns:
            (str): An error message indicating that an unknown error occurred.
        """
        return "Unknown error occurred."

    def get_default_message(self) -> str:
        """
        Get the default error message for a given HTTP status code.

        Returns:
            (str): The default error message associated with the provided status code or unknown error message if not found.
        """
        return http.client.responses.get(self.status_code, self.handle_unknown_error())
