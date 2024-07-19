# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

from typing import Any, Dict, Optional

from requests import Response

from hub_sdk.base.crud_client import CRUDClient
from hub_sdk.base.paginated_list import PaginatedList
from hub_sdk.base.server_clients import DatasetUpload


class Datasets(CRUDClient):
    """
    A class representing a client for interacting with Datasets through CRUD operations.

    This class extends the CRUDClient class and provides specific methods for creating, reading, updating, and deleting
    datasets. It also includes methods for uploading dataset files and retrieving download links.

    Attributes:
        hub_client (DatasetUpload): An instance of DatasetUpload used for interacting with model uploads.
        id (str | None): The unique identifier of the dataset, if available.
        data (dict): A dictionary to store dataset data.

    Methods:
        get_data: Retrieves data for the current dataset instance.
        create_dataset: Creates a new dataset with the provided data and sets the dataset ID for the current instance.
        delete: Deletes the dataset resource represented by this instance, supports soft and hard delete.
        update: Updates the dataset resource represented by this instance with new data.
        upload_dataset: Uploads a dataset file to the hub.
        get_download_link: Retrieves the dataset download link if available.

    Example:
        ```python
        datasets = Datasets(dataset_id='12345')
        dataset_data = {'name': 'new_dataset', 'description': 'Sample dataset'}
        datasets.create_dataset(dataset_data)
        ```

    References:
        [HTTP CRUD Operations](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)
    """

    def __init__(self, dataset_id: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        """
        Initialize a client for interacting with datasets using CRUD operations.

        Args:
            dataset_id (Optional[str]): Unique identifier of the dataset.
            headers (Optional[Dict[str, Any]]): Headers to include in HTTP requests.

        Returns:
            None

        Example:
            ```python
            client = Datasets(dataset_id="12345", headers={"Authorization": "Bearer token"})
            ```
        """
        super().__init__("datasets", "dataset", headers)
        self.hub_client = DatasetUpload(headers)
        self.id = dataset_id
        self.data = {}
        if dataset_id:
            self.get_data()

    def get_data(self) -> None:
        """
        Fetches dataset data for the current dataset instance.

        If a valid dataset ID is set, sends a request to fetch the dataset data and stores it in the instance. If no
        dataset ID is set, logs an error message and returns without any action.

        Args:
            None

        Returns:
            (None): The method does not return a value.

        Example:
            ```python
            datasets_client = Datasets(dataset_id="12345")
            datasets_client.get_data()
            ```
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

    def create_dataset(self, dataset_data: dict) -> None:
        """
        Creates a new dataset with the provided data and sets the dataset ID for the current instance.

        Args:
            dataset_data (dict): A dictionary containing the data for creating the dataset.

        Returns:
            (None): The method does not return a value.

        Example:
            ```python
            dataset_data = {
                'name': 'New Dataset',
                'description': 'A dataset for training object detection models.',
                'labels': ['cat', 'dog']
            }
            datasets = Datasets()
            datasets.create_dataset(dataset_data)
            ```
        """
        resp = super().create(dataset_data).json()
        self.id = resp.get("data", {}).get("id")
        self.get_data()

    def delete(self, hard: bool = False) -> Optional[Response]:
        """
        Deletes the dataset resource represented by this instance.

        Args:
            hard (bool, optional): If True, perform a hard delete. Defaults to False.

        Note:
            The 'hard' parameter determines whether to perform a soft delete (default) or a hard delete.
            In a soft delete, the dataset might be marked as deleted but retained in the system.
            In a hard delete, the dataset is permanently removed from the system.

        Returns:
            (Optional[Response]): Response object from the delete request, or None if delete fails.

        References:
            [Response Processing in Requests](https://docs.python-requests.org/en/master/user/quickstart/#response-content)

        Example:
            ```python
            datasets = Datasets("unique_dataset_id")
            response = datasets.delete(hard=True)
            if response and response.status_code == 204:
                print("Dataset successfully deleted.")
            ```
        """
        return super().delete(self.id, hard)

    def update(self, data: dict) -> Optional[Response]:
        """
        Updates the dataset resource represented by this instance.

        Args:
            data (dict): The updated data for the dataset resource.

        Returns:
            (Optional[Response]): Response object from the update request, or None if update fails.

        Example:
            ```python
            dataset = Datasets("12345")
            update_data = {"name": "New Dataset Name", "description": "Updated description"}
            response = dataset.update(update_data)
            if response:
                print("Dataset updated successfully.")
            ```
        """
        return super().update(self.id, data)

    def upload_dataset(self, file: str = None) -> Optional[Response]:
        """
        Uploads a dataset file to the hub.

        Args:
            file (str, optional): The path to the dataset file to upload.

        Returns:
            (Optional[Response]): Response object from the upload request, or None if upload fails.

        Notes:
            This function uses the `DatasetUpload` client to perform the upload operation.

        References:
            [requests.Response](https://docs.python-requests.org/en/master/api/#requests.Response)

        Example:
            ```python
            dataset_client = Datasets(dataset_id="your-dataset-id")
            response = dataset_client.upload_dataset(file="path/to/your/dataset.zip")
            if response:
                print("Upload successful:", response.json())
            ```
        """
        return self.hub_client.upload_dataset(self.id, file)

    def get_download_link(self) -> Optional[str]:
        """
        Retrieves the download link for the current dataset instance.

        Args:
            None

        Returns:
            (Optional[str]): The download link for the dataset, or None if the link is not available.

        Example:
            ```python
            dataset_client = Datasets(dataset_id="example_id")
            link = dataset_client.get_download_link()
            if link:
                print(f"Download link: {link}")
            else:
                print("Download link not available")
            ```

        Notes:
            Ensure that the dataset ID is set before calling this method.

        References:
            - [Requests library](https://docs.python-requests.org/en/master/)
            - [Optional type hints in Python](https://docs.python.org/3/library/typing.html#typing.Optional)
        """
        return self.data.get("url")


class DatasetList(PaginatedList):
    """
    A DatasetList class for managing and paginating through datasets.

    This class extends the PaginatedList class, providing functionality for handling sequences of dataset items with
    pagination capabilities.

    Attributes:
        endpoint (str): The base API endpoint for datasets.
        page_size (int | None): The number of items to request per page.
        public (bool | None): Whether the datasets should be publicly accessible.
        headers (dict | None): Headers to include in the API requests.

    Methods:
        __init__: Initializes the DatasetList instance with optional pagination and access parameters.

    Example:
        ```python
        dataset_list = DatasetList(page_size=10, public=True)
        for dataset in dataset_list:
            print(dataset["name"])
        ```

    References:
        - [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
    """

    def __init__(self, page_size=None, public=None, headers=None):
        """
        Initializes a DatasetList instance.

        Args:
            page_size (int, optional): The number of items to request per page.
            public (bool, optional): Specifies if the dataset should be publicly accessible.
            headers (dict[str, Any], optional): HTTP headers to include in the requests.

        Returns:
            (None): This method does not return a value.

        Example:
            ```python
            dataset_list = DatasetList(page_size=10, public=True, headers={"Authorization": "Bearer token"})
            ```

        References:
            [Python requests documentation](https://docs.python-requests.org/en/master/user/quickstart/#custom-headers)
        """
        base_endpoint = "datasets"
        super().__init__(base_endpoint, "dataset", page_size, public, headers)
