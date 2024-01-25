# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

from ast import Dict
from typing import Any, Optional
from requests import Response
from hub_sdk.base.crud_client import CRUDClient
from hub_sdk.base.paginated_list import PaginatedList
from hub_sdk.base.server_clients import DatasetUpload
from hub_sdk.config import HUB_FUNCTIONS_ROOT


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

    def __init__(self, dataset_id: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        """
        Initialize a Datasets client.

        Args:
            dataset_id (str): Unique id of the dataset.
            headers (dict, optional): Headers to include in HTTP requests. Defaults to None.
        """
        super().__init__("datasets", "dataset", headers)
        self.hub_client = DatasetUpload(headers)
        self.id = dataset_id
        self.data = {}
        if dataset_id:
            self.get_data()

    def get_data(self) -> None:
        """
        Retrieves data for the current dataset instance.

        If a valid dataset ID has been set, it sends a request to fetch the dataset data and stores it in the instance.
        If no dataset ID has been set, it logs an error message.

        Returns:
            (None)
        """
        if self.id:
            resp = super().read(self.id).json()
            self.data = resp.get("data", {})
            self.logger.debug("Dataset id is %s", self.id)
        else:
            self.logger.error("No dataset id has been set. Update the dataset id or create a dataset.")

    def create_dataset(self, dataset_data: dict) -> None:
        """
        Creates a new dataset with the provided data and sets the dataset ID for the current instance.

        Args:
            dataset_data (dict): A dictionary containing the data for creating the dataset.

        Returns:
            (None)
        """
        resp = super().create(dataset_data).json()
        self.id = resp.get("data", {}).get("id")
        self.get_data()

    def delete(self, hard: bool = False) -> Optional[Response]:
        """
        Delete the dataset using its ID.

        Args:
            hard (bool, optional): Whether to perform a hard delete. Defaults to True.

        Returns:
            (Optional[Response]): Response object from the delete request, or None if delete fails.
        """
        return super().delete(self.id, hard)

    def update(self, data: dict) -> Optional[Response]:
        """
        Update the dataset using its ID.

        Args:
            data (dict): Updated data for the dataset.

        Returns:
            (Optional[Response]): Response object from the update request, or None if update fails.
        """
        return super().update(self.id, data)

    def cleanup(self, id: str) -> Optional[Response]:
        """
        Attempt to delete a dataset by its ID and perform cleanup.

        Args:
            id (str): The ID of the dataset to be deleted.

        Returns:
            (Optional[Response]): Response object from the cleanup request, or None if cleanup fails.
        """
        try:
            return self.delete(f"/{id}")
        except Exception as e:
            self.logger.error("Failed to cleanup: %s", e)

    def upload_dataset(self, file: str = None) -> Optional[Response]:
        """
        Uploads a dataset file to the hub.

        Args:
            file (str, optional): The path to the dataset file to upload. If not provided,
                the method will attempt to upload the default dataset associated with the hub.

        Returns:
            (Optional[Response]): Response object from the upload request, or None if upload fails.
        """
        return self.hub_client.upload_dataset(self.id, file)

    def get_download_link(self, type: str) -> Optional(str):
        """
        Get dataset download link.

        Args:
            type (str):

        Returns:
            (Optional[str]): Return download link or None if the link is not available.
        """
        try:
            payload = {"collection": "datasets", "docId": self.id, "object": type}
            endpoint = f"{HUB_FUNCTIONS_ROOT}/v1/storage"
            response = self.post(endpoint, json=payload)
            json = response.json()
            return json.get("data", {}).get("url")
        except Exception as e:
            self.logger.error(f"Failed to download file file for {self.name}: %s", e)
            raise e


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
