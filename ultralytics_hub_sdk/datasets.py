from .crud_client import CRUDClient
from .paginated_list import PaginatedList


class Datasets(CRUDClient):
    """
    A class representing a client for interacting with datasets through CRUD operations.

    This class extends the CRUDClient class and provides specific methods for working with datasets.

    Args:
        headers (dict, optional): Headers to include in HTTP requests. Defaults to None.

    Attributes:
        base_endpoint (str): The base endpoint for dataset-related API operations.
        item_name (str): The singular name of the dataset resource.
        headers (dict): Headers to include in HTTP requests.

    """

    def __init__(self, arg, headers=None):
        """
        Initialize a Datasets client.

        Args:
            arg (str or dict): Either an ID (string) or data (dictionary) for the dataset.
            headers (dict, optional): Headers to include in HTTP requests. Defaults to None.
        """
        super().__init__("datasets", "dataset", headers)

        if isinstance(arg, str):
            self.id = arg
            resp = super().read(arg)
        elif isinstance(arg, dict):
            resp = super().create(arg)
        
        self.data = resp.get("data",{}) if resp else {}
        self.id = self.data.get('id')

    def __bool__(self):
        """
        Check if the model instance retrieved.
        
        Returns:
            bool: True if self.id, False otherwise.
        """
        return bool(self.id)

    def delete(self, hard=False):
        """
        Delete the dataset using its ID.

        Args:
            hard (bool, optional): Whether to perform a hard delete. Defaults to True.

        Returns:
            dict: The response from the delete request if successful, None otherwise.
        """
        return super().delete(self.id, hard)
    
    def update(self, data):
        """
        Update the dataset using its ID.

        Args:
            data (dict): Updated data for the dataset.

        Returns:
            dict: The response from the update request.
        """
        return super().update(self.id, data)

    def cleanup(self, id):
        """
        Attempt to delete a dataset by its ID and perform cleanup.

        Args:
            id (str): The ID of the dataset to be deleted.

        Returns:
            dict: The response from the delete request if successful, None otherwise.

        Raises:
            Exception: If the delete request fails for any reason.
        """
        try:
            return self._handle_request(self.api_client.delete, f"/{id}")
        except Exception as e:
            self.logger.error('Failed to cleanup: %s', e)


class DatasetList(PaginatedList):
    def __init__(self, page_size=None, public=None, headers=None):
        """
        Initialize a Dataset instance.

        Args:
            page_size (int, optional): The number of items to request per page. Defaults to None.
            public (bool, optional): Whether the items should be publicly accessible. Defaults to None.
            headers (dict, optional): Headers to be included in API requests. Defaults to None.
        """
        base_endpoint = "datasets"
        if public:
            base_endpoint = f"public/{base_endpoint}"
        super().__init__(base_endpoint, "dataset", page_size, headers)
