class ErrorHandler:
    def __init__(self, status_code):
        self.status_code = status_code

    def handle(self):
        error_handlers = {
            401: self.handle_unauthorized,
            404: self.handle_not_found,
            500: self.handle_internal_server_error,
        }

        handler = error_handlers.get(self.status_code, self.handle_unknown_error)
        return handler(self)

    @staticmethod
    def handle_unauthorized(self):
        return "Unauthorized: Please check your credentials."

    @staticmethod
    def handle_not_found(self):
        return "Resource not found."

    @staticmethod
    def handle_internal_server_error(self):
        return "Internal server error."

    @staticmethod
    def handle_unknown_error(self):
        return "Unknown error occurred."
