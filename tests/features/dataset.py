from tests.utils.base_class import BaseClass


class Dataset(BaseClass):
    """
    A Dataset class for managing datasets, including creation, retrieval, updates, and deletions.

    This class provides methods to interact with dataset objects, allowing for CRUD operations, checking
    dataset existence, and retrieving specific dataset information.

    Attributes:
        client (object): The client object to interact with the dataset service.

    Methods:
        get_dataset_by_id(dataset_id): Retrieves a dataset by its ID.
        create_new_dataset(data): Creates a new dataset with the provided data and returns its ID.
        is_dataset_exists(dataset_id): Checks if a dataset with the specified ID exists.
        update_dataset(dataset_id, data): Updates an existing dataset with the provided data.
        get_dataset_name(dataset_id): Retrieves the name of a dataset based on its ID.
        delete_dataset(dataset_id): Deletes a dataset based on its ID.
        list_public_datasets(): Retrieves a list of public datasets.
        get_dataset_download_link(dataset_id): Retrieves the download link for a specific dataset.
        upload_dataset_file(dataset_id, dataset_file): Uploads a dataset file for a specific dataset.

    Example:
        ```python
        client = DatasetClient(api_key='YOUR_API_KEY')
        dataset_service = Dataset(client=client)

        # Creating a new dataset
        new_dataset_id = dataset_service.create_new_dataset(data={'name': 'example', 'description': 'test dataset'})

        # Retrieving a dataset by ID
        dataset = dataset_service.get_dataset_by_id(new_dataset_id)

        # Checking dataset existence
        exists = dataset_service.is_dataset_exists(new_dataset_id)
        ```

    References:
        - [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
        - [Dataset API Documentation](https://example.com/dataset-api-docs)
    """

    def __init__(self, client):
        """
        Initializes Dataset with a specified client object for data operations.

        Args:
            client (object): Client instance used for dataset operations.

        Returns:
            None

        Notes:
            The client object must support necessary dataset functionalities including fetching and storing data.

        Example:
            ```python
            from some_data_client import DataClient
            client = DataClient(api_key='your_api_key')
            dataset = Dataset(client)
            ```

        References:
            [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
        """
        self.client = client

    def get_dataset_by_id(self, dataset_id):
        """
        Retrieves a dataset by its unique identifier.

        Args:
            dataset_id (str): The unique identifier string of the dataset to be retrieved.

        Returns:
            (Dataset): The dataset object associated with the provided ID.

        Example:
            ```python
            client = SomeClientObject()
            dataset = Dataset(client)
            data = dataset.get_dataset_by_id("12345")
            ```

        References:
            - [Python string methods](https://docs.python.org/3/library/stdtypes.html#string-methods)
        """
        self.delay()
        return self.client.dataset(dataset_id)

    def create_new_dataset(self, data):
        """
        Creates a new dataset with the provided data.

        Args:
            data (dict): The data to create the dataset.

        Returns:
            (str): The ID of the newly created dataset.

        Notes:
            Ensure the `data` dictionary conforms to the expected schema for dataset creation to avoid errors during
            the creation process.
        """
        self.delay()
        dataset = self.client.dataset()
        self.delay()
        dataset.create_dataset(data)
        return dataset.id

    def is_dataset_exists(self, dataset_id):
        """
        Checks if a dataset with the specified ID exists.

        Args:
            dataset_id (str): The ID of the dataset.

        Returns:
            (bool): True if the dataset exists, False otherwise.

        Notes:
            This function will log an error if an exception is encountered during the existence check.

        Example:
            ```python
            dataset = Dataset(client)
            does_exist = dataset.is_dataset_exists("dataset123")
            ```

        References:
            [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
            [Dataset API Documentation](https://docs.example.com/dataset-api)
        """
        try:
            dataset = self.get_dataset_by_id(dataset_id)
            return bool(dataset.data)
        except Exception as e:
            log = self.get_logger()
            log.error(e)
            return False

    def update_dataset(self, dataset_id, data):
        """
        Updates an existing dataset with the provided data.

        Args:
            dataset_id (str): The ID of the dataset to update.
            data (dict): The data to update the dataset.

        Returns:
            (bool): True if the update is successful, False otherwise.

        Example:
            ```python
            dataset_id = "12345"
            data = {"name": "New Dataset Name", "description": "Updated description"}
            success = dataset.update_dataset(dataset_id, data)
            ```

        Notes:
            It's important to ensure the dataset ID is valid and the data dictionary follows the required schema
            for updates.

        References:
            [Python's requests library](https://docs.python-requests.org/en/latest/)
        """
        dataset = self.get_dataset_by_id(dataset_id)
        self.delay()
        dataset.update(data)

    def get_dataset_name(self, dataset_id):
        """
        Retrieves the name of a dataset based on its ID.

        Args:
            dataset_id (str): The ID of the dataset.

        Returns:
            (str): The name of the dataset.

        Example:
            ```python
            dataset = Dataset(client)
            dataset_name = dataset.get_dataset_name('12345')
            ```
        """
        return self.get_dataset_by_id(dataset_id).data["meta"]["name"]

    def delete_dataset(self, dataset_id):
        """
        Deletes a dataset based on its ID.

        Args:
            dataset_id (str): The ID of the dataset to delete.

        Returns:
            None

        Notes:
            This function will raise an exception if the dataset cannot be found or if there is an error during
            the deletion process. Ensure proper exception handling when using this function.

        References:
            For more information on common exceptions in Python, visit the
            [Python Exceptions Tutorial](https://docs.python.org/3/tutorial/errors.html).
        """
        dataset = self.get_dataset_by_id(dataset_id)
        self.delay()
        dataset.delete(hard=True)

    def list_public_datasets(self):
        """
        Retrieves a list of public datasets.

        Args:
            None

        Returns:
            (list[dict]): A list of dictionaries where each dictionary represents a public dataset, limited to
                a page size of 10.

        Example:
            ```python
            dataset_instance = Dataset(client)
            public_datasets = dataset_instance.list_public_datasets()
            ```

        Notes:
            This method limits the retrieved datasets to a page size of 10 for efficiency.

        References:
            - [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
            - [REST API Documentation](https://restfulapi.net)
        """
        self.delay()
        dataset_list = self.client.dataset_list(page_size=10, public=True)
        return dataset_list.results

    def get_dataset_download_link(self, dataset_id):
        """
        Retrieves the download link for a specific dataset.

        Args:
            dataset_id (str): The ID of the dataset.

        Returns:
            (str): The download link for the dataset.

        Example:
            ```python
            dataset = Dataset(client)
            download_link = dataset.get_dataset_download_link("1234")
            ```
        """
        dataset = self.get_dataset_by_id(dataset_id)
        self.delay()
        return dataset.get_download_link()

    def upload_dataset_file(self, dataset_id, dataset_file):
        """
        Uploads a dataset file for a specific dataset.

        Args:
            dataset_id (str): The ID of the dataset.
            dataset_file: The file containing the dataset data.

        Returns:
            (None): Does not return anything.

        Notes:
            This function will delay operations as needed before uploading the dataset file.
        """
        dataset = self.get_dataset_by_id(dataset_id)
        self.delay()
        dataset.upload_dataset(file=dataset_file)
