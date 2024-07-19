import pytest

from tests.features.object_manager import ObjectManager
from tests.test_data.data import TestData
from tests.utils.base_class import BaseClass


class TestDataset(BaseClass):
    """
    A TestDataset class for performing dataset operations in a testing environment.

    This class encapsulates various test cases for dataset operations such as retrieval, creation, updating metadata,
    deletion, listing, and storage URL retrieval. Each method is decorated with `pytest.mark.smoke` to denote critical
    test cases.

    Attributes:
        client (Any): The client interface used for interfacing with the dataset manager.
        cache (Any): A caching mechanism for storing temporary data, typically provided by `pytest`.

    Methods:
        test_dataset_001: Verify successful retrieval of a dataset by ID.
        test_dataset_002: Verify successful creation of a new dataset.
        test_dataset_003: Verify successful update of dataset metadata.
        test_dataset_004: Verify successful deletion of a dataset.
        test_dataset_005: Verify successful listing of datasets.
        test_dataset_006: Verify successful retrieval of dataset storage URL.
        test_dataset_007: Verify successful upload of a dataset.

    Example:
        ```python
        import pytest
        from TestDataset import TestDataset

        class TestClient:
            # Mock client implementation
            pass

        @pytest.fixture
        def client():
            return TestClient()

        dataset_tester = TestDataset()
        dataset_tester.client = client
        dataset_tester.test_dataset_001()
        ```

    References:
        [Pytest Documentation](https://docs.pytest.org/en/stable/)
    """

    @pytest.mark.smoke
    def test_dataset_001(self):
        """
        Verify successful retrieval of a dataset by ID.

        Args:
            None

        Returns:
            None

        References:
            [Pytest Documentation](https://docs.pytest.org/en/stable/)

        Example:
            To run this test, use the following command:
            ```bash
            pytest path/to/your/test_file.py::TestDataset::test_dataset_001
            ```

        Notes:
            This is a smoke test to ensure that dataset retrieval functionality is working as expected.
        """

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
        """
        Verify successful creation of a new dataset.

        Args:
            request (pytest.FixtureRequest): The request fixture provides information about the requesting test function.
            delete_test_dataset (bool): A fixture to signal cleanup after test execution.

        Returns:
            None

        Example:
            ```python
            def test_create_dataset(request, delete_test_dataset):
                test_dataset_instance = TestDataset()
                test_dataset_instance.test_dataset_002(request, delete_test_dataset)
            ```

        Notes:
            Ensure `delete_test_dataset` fixture is properly configured to handle test cleanup.

        References:
            [pytest Documentation](https://docs.pytest.org/en/stable/)
        """

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
        """
        Verify successful update of dataset metadata.

        Args:
            request (pytest.FixtureRequest): A request for obtaining the test name and accessing the cache.
            create_test_dataset (pytest.fixture): Fixture that ensures creation of a test dataset before the test.
            delete_test_dataset (pytest.fixture): Fixture that ensures deletion of a test dataset after the test.

        Returns:
            (None)

        Example:
            ```python
            def test_dataset_003(self, request, create_test_dataset, delete_test_dataset):
                # Execute test to verify dataset metadata update
            ```

        References:
            [pytest documentation](https://docs.pytest.org/en/6.2.x/contents.html)
        """

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

        assert (
            updated_dataset_name == desired_dataset_name
        ), f"Dataset name is not updated as expected. Actual: {updated_dataset_name}, Expected: {desired_dataset_name}"

    @pytest.mark.smoke
    def test_dataset_004(self, request, create_test_dataset):
        """
        Verifies successful deletion of a dataset.

        Args:
            request (pytest.FixtureRequest): The pytest fixture request object used to access test metadata.
            create_test_dataset (function): Pytest fixture to create a dataset for testing.

        Returns:
            (None): This function does not return any value.

        Example:
            ```python
            def test_dataset_004(self, request, create_test_dataset):
                # Expected to log info and assert successful deletion
                ```
        """

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
        assert not dataset_obj.is_dataset_exists(
            dataset_id
        ), f"Dataset with ID {dataset_id} still exists after deletion."

    @pytest.mark.smoke
    def test_dataset_005(self):
        """
        Verify successful listing of datasets.

        Args:
            None

        Returns:
            (list[dict]): List of public datasets, where each dataset is represented as a dictionary containing
            dataset metadata.

        Example:
            ```python
            test_instance = TestDataset()
            public_datasets = test_instance.test_dataset_005()
            # Example assertion to confirm dataset listing contains expected keys
            assert "id" in public_datasets[0], "ID information not found in the dataset data"
            ```

        Notes:
            - This method is designed to be run as part of a pytest suite. It is marked with the pytest.smoke marker
              for quick, basic validation.

        References:
            - [pytest documentation](https://docs.pytest.org/en/stable/)
        """

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
        """
        Verify successful retrieval of dataset storage URL.

        Args:
            None

        Returns:
            (str): URL for downloading the dataset with the specified ID.

        Example:
            ```python
            test_dataset = TestDataset()
            storage_url = test_dataset.test_dataset_006()
            ```

        Notes:
            This function specifically tests if the dataset storage URL can be successfully retrieved.

        References:
            [Pytest Documentation](https://docs.pytest.org/en/stable/)
        """

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
        """
        Verify successful upload of a dataset.

        Args:
            request (_pytest.fixtures.FixtureRequest): The pytest FixtureRequest object.
            create_test_dataset (fixture): A pytest fixture to create a test dataset.
            delete_test_dataset (fixture): A pytest fixture to delete a test dataset.

        Returns:
            None

        Example:
            ```python
            def test_dataset_upload(request, create_test_dataset, delete_test_dataset):
                test_instance = TestDataset()
                test_instance.test_dataset_007(request, create_test_dataset, delete_test_dataset)
            ```
        """

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
