from tests.utils.base_class import BaseClass


class Dataset(BaseClass):
    """A class for managing datasets with methods for creation, retrieval, updating, deletion, and file uploads."""

    def __init__(self, client):
        """Initializes Dataset with a specified client object, storing it for future use."""
        self.client = client

    def get_dataset_by_id(self, dataset_id):
        """
        Retrieves a dataset by its ID.

        Args:
            dataset_id (str): The ID of the dataset.

        Returns:
            Dataset: The dataset object.
        """
        self.delay()
        return self.client.dataset(dataset_id)

    def create_new_dataset(self, data):
        """
        Creates a new dataset with the provided data.

        Args:
            data (dict): The data to create the dataset.

        Returns:
            str: The ID of the newly created dataset.
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
            bool: True if the dataset exists, False otherwise.
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
            str: The name of the dataset.
        """
        return self.get_dataset_by_id(dataset_id).data["meta"]["name"]

    def delete_dataset(self, dataset_id):
        """
        Deletes a dataset based on its ID.

        Args:
            dataset_id (str): The ID of the dataset to delete.
        """
        dataset = self.get_dataset_by_id(dataset_id)
        self.delay()
        dataset.delete(hard=True)

    def list_public_datasets(self):
        """
        Retrieves a list of public datasets.

        Returns:
            list: A list of public datasets, limited to a page size of 10.
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
            str: The download link for the dataset.
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
        """
        dataset = self.get_dataset_by_id(dataset_id)
        self.delay()
        dataset.upload_dataset(file=dataset_file)
