from .crud_client import CRUDClient


class Teams(CRUDClient):
    """
    A class representing CRUD operations for managing teams.
    
    This class extends the CRUDClient class to provide specific functionality
    for managing teams. It inherits common CRUD (Create, Read, Update, Delete)
    operations from the parent class.
    
    Args:
        headers (dict, optional): Headers to be included in the API requests.

    Attributes:
        entity_type (str): The type of entity being managed (e.g., "team").
    """
    def __init__(self, headers=None):
        """
        Initialize a Teams instance.

        Args:
            headers (dict, optional): Headers to be included in the API requests.
        """
        super().__init__("teams", "team", headers)


    def cleanup(self, id):
        """
        Clean up a team by deleting it from the system.

        This method sends a delete request to the API to remove the team with
        the specified ID.

        Args:
            id (int): The ID of the team to be cleaned up.

        Returns:
            dict: The response from the delete request.

        Raises:
            Exception: If the delete request fails.
        """
        try:
            return self._handle_request(self.api_client.delete, f"/{id}")
        except Exception as e:
            self.logger.error('Failed to cleanup: %s', e)
