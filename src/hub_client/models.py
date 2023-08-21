from .crud_client import CRUDClient


class Models(CRUDClient):
    def __init__(self, headers=None):
        """
        Initialize a Models instance.

        Args:
            headers (dict, optional): Headers to be included in API requests. Defaults to None.
        """
        super().__init__("models", "model", headers)


    def cleanup(self, id):
        """
        Delete a model resource by its ID.

        This method sends a DELETE request to the API to delete the model resource with the specified ID.

        Args:
            id (int): The ID of the model resource to be deleted.

        Returns:
            dict: A dictionary containing the API response data after the deletion.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        try:
            return self._handle_request(self.api_client.delete, f"/{id}")
        except Exception as e:
            self.logger.error('Failed to cleanup: %s', e)
