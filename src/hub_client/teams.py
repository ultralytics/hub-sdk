from .crud_client import CRUDClient
from .paginated_list import PaginatedList


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
    def __init__(self, arg, headers=None):
        """
        Initialize a Teams instance.

        Args:
            arg (str or dict): Either an ID (string) or data (dictionary) for the team.
            headers (dict, optional): Headers to be included in the API requests.
        """
        super().__init__("teams", "team", headers)

        if isinstance(arg, str):
            self.id = arg
            resp = super().read(arg)
        elif isinstance(arg, dict):
            resp = super().create(arg)
        
        self.data = resp.get("data",{}) if resp else {}
        self.id = self.data.get('id')

    def delete(self, hard=False):
        """
        Delete the team.

        Args:
            hard (bool, optional): If True, perform a hard delete. Defaults to True.

        Returns:
            dict: The response from the delete request.
        """
        return super().delete(self.id, hard)

    def update(self, data):
        """
        Update the team's data.

        Args:
            data (dict): The updated data for the team.

        Returns:
            dict: The response from the update request.
        """
        return super().update(self.id, data)

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

class TeamList(PaginatedList):
    def __init__(self, page_size=None, public=None, headers=None):
        """
        Initialize a TeamList instance.

        Args:
            page_size (int, optional): The number of items to request per page. Defaults to None.
            public (bool, optional): Whether the items should be publicly accessible. Defaults to None.
            headers (dict, optional): Headers to be included in API requests. Defaults to None.
        """
        base_endpoint = "datasets"
        if public:
            base_endpoint = f"public/{base_endpoint}"
        super().__init__(base_endpoint, "team", page_size, headers)
