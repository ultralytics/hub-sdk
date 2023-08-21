from .crud_client import CRUDClient


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

    Methods:
        __init__(headers=None):
            Initialize the Datasets client with the given headers.

        cleanup(id):
            Attempt to delete a dataset by its ID and perform cleanup.
            Args:
                id (str): The ID of the dataset to be deleted.
            Returns:
                dict: The response from the delete request if successful, None otherwise.
            Raises:
                Exception: If the delete request fails for any reason.
    """
    def __init__(self, headers=None):
        """
        Initialize a Datasets client.

        Args:
            headers (dict, optional): Headers to include in HTTP requests. Defaults to None.
        """
        super().__init__("datasets", "dataset", headers)


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
