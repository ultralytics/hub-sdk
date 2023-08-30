from .crud_client import CRUDClient


class Projects(CRUDClient):
    def __init__(self, headers=None):
        """
        Initialize a Projects object for interacting with project data via CRUD operations.

        Args:
            headers (dict, optional): A dictionary of HTTP headers to be included in API requests.
                                      Defaults to None.
        """
        super().__init__("projects", "project", headers)


    def cleanup(self, id):
        """
        Attempt to delete a project's data from the server.

        This method sends a DELETE request to the server in order to clean up a project's data.
        If the deletion is successful, the project's data will be removed from the server.

        Args:
            id (int or str): The unique identifier of the project to be cleaned up.

        Returns:
            dict: A dictionary containing the response data from the server if the cleanup
                  operation was successful.
                  None if the operation fails.

        Raises:
            Exception: If there is an issue with the API request or response during cleanup.
        """
        try:
            return self._handle_request(self.api_client.delete, f"/{id}")
        except Exception as e:
            self.logger.error('Failed to cleanup: %s', e)
