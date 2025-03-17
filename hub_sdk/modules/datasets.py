# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from typing import Any, Dict, Optional

from requests import Response

from hub_sdk.base.crud_client import CRUDClient
from hub_sdk.base.paginated_list import PaginatedList
from hub_sdk.base.server_clients import DatasetUpload


class Datasets(CRUDClient):
    """
    A class representing a client for interacting with Datasets through CRUD operations.

    This class extends the CRUDClient class and provides specific methods for working with Datasets.

    Attributes:
        hub_client (DatasetUpload): An instance of DatasetUpload used for interacting with dataset uploads.
        id (str | None): The unique identifier of the dataset, if available.
        data (Dict): A dictionary to store dataset data.

    Note:
        The 'id' attribute is set during initialization and can be used to uniquely identify a dataset.
        The 'data' attribute is used to store dataset data fetched from the API.
    """

    def __init__(self, dataset_id: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        """
        Initialize a Datasets client.

        Args:
            dataset_id (str, optional): Unique id of the dataset.
            headers (Dict, optional): Headers to include in HTTP requests.
        """
        super().__init__("datasets", "dataset", headers)
        self.hub_client = DatasetUpload(headers)
        self.id = dataset_id
        self.data = {}
        if dataset_id:
            self.get_data()

    def get_data(self) -> None:
        """
        Retrieve data for the current dataset instance.

        If a valid dataset ID has been set, it sends a request to fetch the dataset data and stores it in the instance.
        If no dataset ID has been set, it logs an error message.
        """
        if not self.id:
            self.logger.error("No dataset id has been set. Update the dataset id or create a dataset.")
            return

        try:
            response = super().read(self.id)

            if response is None:
                self.logger.error(f"Received no response from the server for dataset ID: {self.id}")
                return

            # Check if the response has a .json() method (it should if it's a response object)
            if not hasattr(response, "json"):
                self.logger.error(f"Invalid response object received for dataset ID: {self.id}")
                return

            resp_data = response.json()
            if resp_data is None:
                self.logger.error(f"No data received in the response for dataset ID: {self.id}")
                return

            self.data = resp_data.get("data", {})
            self.logger.debug(f"Dataset data retrieved for ID: {self.id}")

        except Exception as e:
            self.logger.error(f"An error occurred while retrieving data for dataset ID: {self.id}, {e}")

    def create_dataset(self, dataset_data: Dict) -> None:
        """
        Create a new dataset with the provided data and set the dataset ID for the current instance.

        Args:
            dataset_data (Dict): A dictionary containing the data for creating the dataset.
        """
        resp = super().create(dataset_data).json()
        self.id = resp.get("data", {}).get("id")
        self.get_data()

    def delete(self, hard: bool = False) -> Optional[Response]:
        """
        Delete the dataset resource represented by this instance.

        Args:
            hard (bool, optional): If True, perform a hard delete.

        Note:
            The 'hard' parameter determines whether to perform a soft delete (default) or a hard delete.
            In a soft delete, the dataset might be marked as deleted but retained in the system.
            In a hard delete, the dataset is permanently removed from the system.

        Returns:
            (Optional[Response]): Response object from the delete request, or None if delete fails.
        """
        return super().delete(self.id, hard)

    def update(self, data: Dict) -> Optional[Response]:
        """
        Update the dataset resource represented by this instance.

        Args:
            data (Dict): The updated data for the dataset resource.

        Returns:
            (Optional[Response]): Response object from the update request, or None if update fails.
        """
        return super().update(self.id, data)

    def upload_dataset(self, file: str = None) -> Optional[Response]:
        """
        Upload a dataset file to the hub.

        Args:
            file (str, optional): The path to the dataset file to upload.

        Returns:
            (Optional[Response]): Response object from the upload request, or None if upload fails.
        """
        return self.hub_client.upload_dataset(self.id, file)

    def get_download_link(self) -> Optional[str]:
        """
        Get dataset download link.

        Returns:
            (Optional[str]): Return download link or None if the link is not available.
        """
        return self.data.get("url")


class DatasetList(PaginatedList):
    """A class for managing a paginated list of datasets from the Ultralytics Hub API."""

    def __init__(self, page_size=None, public=None, headers=None):
        """
        Initialize a DatasetList instance.

        Args:
            page_size (int, optional): The number of items to request per page.
            public (bool, optional): Whether the items should be publicly accessible.
            headers (Dict, optional): Headers to be included in API requests.
        """
        base_endpoint = "datasets"
        super().__init__(base_endpoint, "dataset", page_size, public, headers)
