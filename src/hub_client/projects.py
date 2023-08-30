from .crud_client import CRUDClient
from .paginated_list import PaginatedList

class Projects(CRUDClient):
    def __init__(self, arg, headers=None):
        """
        Initialize a Projects object for interacting with project data via CRUD operations.

        Args:
            arg (str or dict): Either an ID (string) or data (dictionary) for the project.
            headers (dict, optional): A dictionary of HTTP headers to be included in API requests.
                                      Defaults to None.
        """
        super().__init__("projects", "project", headers)

        if isinstance(arg, str):
            self.id = arg
            resp = super().read(arg)
        elif isinstance(arg, dict):
            resp = super().create(arg)
        
        self.data = resp.get("data",{})
        self.id = self.data.get('id')

    def delete(self, hard=False):
        """
        Delete the project.

        Args:
            hard (bool, optional): If True, perform a hard delete. If False, perform a soft delete.
                                   Defaults to True.

        Returns:
            dict: A dictionary containing the response data from the server if the delete
                  operation was successful.
                  None if the operation fails.
        """
        return super().delete(self.id, hard)

    def update(self, data):
        """
        Update the project's data.

        Args:
            data (dict): The updated data for the project.

        Returns:
            dict: A dictionary containing the response data from the server if the update
                  operation was successful.
                  None if the operation fails.
        """
        return super().update(self.id, data)

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

class ProjectList(PaginatedList):
    def __init__(self, page_size=None, public=None, headers=None):
        """
        Initialize a ProjectList instance.

        Args:
            page_size (int, optional): The number of items to request per page. Defaults to None.
            public (bool, optional): Whether the items should be publicly accessible. Defaults to None.
            headers (dict, optional): Headers to be included in API requests. Defaults to None.
        """
        base_endpoint = "projects"
        if public:
            base_endpoint = f"public/{base_endpoint}" 
        super().__init__(base_endpoint, "project", page_size, headers)
