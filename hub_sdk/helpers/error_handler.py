# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

import http.client
from typing import Optional


class ErrorHandler:
    """
    Represents an error handler for managing HTTP status codes and error messages.

    Attributes:
        status_code (int): The HTTP status code associated with the error.
        message (str, None): An optional error message providing additional details.
            Defaults to None.
    """

    def __init__(self, status_code: int, message: Optional[str] = None):
        """
        Initialize the ErrorHandler object with a given status code.

        Args:
            status_code (int): The HTTP status code representing the error.
            message (str, optional): An optional error message providing additional details.
        """
        self.status_code = status_code
        self.message = message

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
        }

        handler = error_handlers.get(self.status_code, self.get_default_message)
        return handler()

    def handle_unauthorized(self) -> str:
        """
        Handle an unauthorized error (HTTP 401).

        Returns:
            (str): An error message indicating unauthorized access.
        """
        return "Unauthorized: Please check your credentials."

    def handle_not_found(self) -> str:
        """
        Handle a resource not found error (HTTP 404).

        Returns:
            (str): An error message indicating that the requested resource was not found.
        """
        return "Resource not found."

    def handle_internal_server_error(self) -> str:
        """
        Handle an internal server error (HTTP 500).

        Returns:
            (str): An error message indicating an internal server error.
        """
        return "Internal server error."

    def handle_unknown_error(self) -> str:
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
            (str): The default error message associated with the provided status code.
                 If no message is found, it falls back to handling an unknown error.
        """
        return http.client.responses.get(self.status_code, self.handle_unknown_error())
