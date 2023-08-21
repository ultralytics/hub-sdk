class ErrorHandler:
    def __init__(self, status_code):
        """
        Initialize the ErrorHandler object with a given status code.

        :param status_code: The HTTP status code representing the error.
        """
        self.status_code = status_code

    def handle(self):
        """
        Handle the error based on the provided status code.

        :return: A message describing the error.
        """
        error_handlers = {
            401: self.handle_unauthorized,
            404: self.handle_not_found,
            500: self.handle_internal_server_error,
        }

        handler = error_handlers.get(self.status_code, self.handle_unknown_error)
        return handler(self)

    @staticmethod
    def handle_unauthorized(self):
        """
        Handle an unauthorized error (HTTP 401).

        :return: An error message indicating unauthorized access.
        """
        return "Unauthorized: Please check your credentials."

    @staticmethod
    def handle_not_found(self):
        """
        Handle a resource not found error (HTTP 404).

        :return: An error message indicating that the requested resource was not found.
        """
        return "Resource not found."

    @staticmethod
    def handle_internal_server_error(self):
        """
        Handle an internal server error (HTTP 500).

        :return: An error message indicating an internal server error.
        """
        return "Internal server error."

    @staticmethod
    def handle_unknown_error(self):
        """
        Handle an unknown error.

        :return: An error message indicating that an unknown error occurred.
        """
        return "Unknown error occurred."
