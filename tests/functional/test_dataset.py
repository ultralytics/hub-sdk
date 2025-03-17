# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import pytest

from tests.features.object_manager import ObjectManager
from tests.test_data.data import TestData
from tests.utils.base_class import BaseClass


class TestDataset(BaseClass):
    """
    Class for testing dataset operations: retrieval, creation, update, deletion, listing, and upload with pytest.

    This class contains test methods for verifying the functionality of dataset operations using the Ultralytics API.
    Each test method focuses on a specific operation such as retrieving datasets, creating new datasets, updating
    dataset metadata, deleting datasets, listing datasets, and uploading dataset files.

    Attributes:
        client: The API client used for making requests to the Ultralytics API.

    Methods:
        test_dataset_001: Verify successful retrieval of a dataset by ID.
        test_dataset_002: Verify successful creation of a new dataset.
        test_dataset_003: Verify successful update of dataset metadata.
        test_dataset_004: Verify successful deletion of a dataset.
        test_dataset_005: Verify successful listing of datasets.
        test_dataset_006: Verify successful retrieval of dataset storage URL.
        test_dataset_007: Verify successful upload of a dataset.
    """

    @pytest.mark.smoke
    def test_dataset_001(self):
        """Verify successful retrieval of a dataset by ID."""
        log = self.get_logger()
        dataset_id = TestData().get_datasets_data()["valid_dataset_ID"]
        log.info(f"Attempting to retrieve dataset with ID: {dataset_id}")

        object_manager = ObjectManager(self.client)
        dataset_obj = object_manager.get_dataset()
        dataset = dataset_obj.get_dataset_by_id(dataset_id)

        log.info(f"Dataset retrieved successfully. Dataset data: {dataset.data}")

        assert "id" in dataset.data, "ID information not found in the dataset data"
        assert "meta" in dataset.data, "Meta information not found in the dataset data"

    @pytest.mark.smoke
    def test_dataset_002(self, request, delete_test_dataset):
        """Verify successful creation of a new dataset."""
        log = self.get_logger()

        new_dataset_data = TestData().get_datasets_data()["new_dataset_data"]
        log.info(f"Attempting to create a new dataset with data: {new_dataset_data}")

        object_manager = ObjectManager(self.client)
        dataset_obj = object_manager.get_dataset()

        # Create new dataset
        dataset_id = dataset_obj.create_new_dataset(new_dataset_data)

        log.info(f"New dataset created successfully. Dataset ID: {dataset_id}")

        # Set the dataset_id in the cache with a key that includes the test name
        test_name = request.node.name
        dataset_id_key = f"dataset_id_for_test_{test_name}"
        request.config.cache.set(dataset_id_key, dataset_id)

        log.info(f"Verifying dataset exists with dataset ID: {dataset_id}")
        assert dataset_obj.is_dataset_exists(dataset_id), f"Dataset not exists with dataset ID: {dataset_id}"
        log.info(f"Dataset exists with dataset ID: {dataset_id}")

    @pytest.mark.smoke
    def test_dataset_003(self, request, create_test_dataset, delete_test_dataset):
        """Verify successful update of dataset metadata."""
        log = self.get_logger()

        # Retrieve necessary data
        test_name = request.node.name
        dataset_id_key = f"dataset_id_for_{test_name}"
        dataset_id = request.config.cache.get(dataset_id_key, None)
        desired_dataset_data = TestData().get_datasets_data()["desired_dataset_data"]
        desired_dataset_name = desired_dataset_data["meta"]["name"]

        log.info(
            f"Attempting to update metadata for dataset with ID {dataset_id}. Desired dataset data: "
            f"{desired_dataset_data}"
        )

        object_manager = ObjectManager(self.client)
        dataset_obj = object_manager.get_dataset()

        # Update dataset metadata
        dataset_obj.update_dataset(dataset_id, desired_dataset_data)

        log.info("Dataset metadata updated successfully.")

        # Get the updated dataset name
        updated_dataset_name = dataset_obj.get_dataset_name(dataset_id)

        log.info(f"Updated dataset name: {updated_dataset_name}")

        assert updated_dataset_name == desired_dataset_name, (
            f"Dataset name is not updated as expected. Actual: {updated_dataset_name}, Expected: {desired_dataset_name}"
        )

    @pytest.mark.smoke
    def test_dataset_004(self, request, create_test_dataset):
        """Verify successful deletion of a dataset."""
        log = self.get_logger()

        # Retrieve necessary data
        test_name = request.node.name
        dataset_id_key = f"dataset_id_for_{test_name}"
        dataset_id = request.config.cache.get(dataset_id_key, None)

        log.info(f"Attempting to delete dataset with ID: {dataset_id}")

        object_manager = ObjectManager(self.client)
        dataset_obj = object_manager.get_dataset()

        # Delete the dataset
        dataset_obj.delete_dataset(dataset_id)

        log.info("Dataset deleted successfully.")

        # Verify if the dataset no longer exists
        assert not dataset_obj.is_dataset_exists(dataset_id), (
            f"Dataset with ID {dataset_id} still exists after deletion."
        )

    @pytest.mark.smoke
    def test_dataset_005(self):
        """Verify successful listing of datasets."""
        log = self.get_logger()

        log.info("Attempting to list public datasets.")

        object_manager = ObjectManager(self.client)
        dataset_obj = object_manager.get_dataset()

        # List public datasets
        public_dataset_list = dataset_obj.list_public_datasets()

        log.info(f"Public datasets listed successfully. First dataset information: {public_dataset_list[0]}")

        assert "id" in public_dataset_list[0], "ID information not found in the dataset data"
        assert "meta" in public_dataset_list[0], "Meta information not found in the dataset data"

    @pytest.mark.smoke
    def test_dataset_006(self):
        """Verify successful retrieval of dataset storage URL."""
        log = self.get_logger()

        log.info("Attempting to retrieve dataset storage URL.")

        object_manager = ObjectManager(self.client)
        dataset_obj = object_manager.get_dataset()

        dataset_id = TestData().get_datasets_data()["valid_dataset_ID"]

        # Get Dataset storage URL
        link = dataset_obj.get_dataset_download_link(dataset_id)

        log.info(f"Dataset storage URL retrieved successfully: {link}")

        assert f"{dataset_id}" in link

    @pytest.mark.smoke
    def test_dataset_007(self, request, create_test_dataset, delete_test_dataset):
        """Verify successful upload of a dataset."""
        log = self.get_logger()

        # Retrieve necessary data
        test_name = request.node.name
        dataset_id_key = f"dataset_id_for_{test_name}"
        dataset_id = request.config.cache.get(dataset_id_key, None)
        dataset_file = TestData().get_datasets_data()["dataset_file"]

        log.info(f"Attempting to upload dataset file for dataset with ID {dataset_id}. Dataset file: {dataset_file}")

        object_manager = ObjectManager(self.client)
        dataset_obj = object_manager.get_dataset()

        # Upload dataset file
        dataset_obj.upload_dataset_file(dataset_id, dataset_file)

        log.info("Dataset file uploaded successfully.")
        # Get the dataset storage URL
        link = dataset_obj.get_dataset_download_link(dataset_id)

        log.info(f"Dataset storage URL retrieved: {link}")

        assert f"{dataset_id}/{dataset_file.split('/')[-1]}" in link
