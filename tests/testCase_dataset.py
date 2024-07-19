# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

import unittest

from hub_sdk import HUBClient


class TestDatasetSDK(unittest.TestCase):
    """
    A `TestDatasetSDK` class for testing Ultralytics HUB-SDK dataset functionalities using the `unittest` framework.

    Attributes:
        client (HUBClient): Instance of `HUBClient` initialized with user credentials.
        dataset (Dataset): Dataset instance retrieved from `HUBClient`.

    Methods:
        setUp: Initializes the `HUBClient` instance and the dataset before each test.
        test_create_dataset: Tests the creation of a dataset using `HUBClient`.
        test_get_dataset_by_id: Tests retrieval of a dataset by its ID using `HUBClient`.
        test_update_dataset: Tests updating a dataset's information using `HUBClient`.
        test_list_datasets: Tests listing available datasets using `HUBClient`.
        test_upload_dataset: Tests the upload functionality for datasets using `HUBClient`.
        test_get_download_link: Tests retrieval of download link for a dataset using `HUBClient`.
        test_delete_dataset: Tests the deletion functionality of a dataset using `HUBClient`.

    References:
        - [unittest](https://docs.python.org/3/library/unittest.html): Python's built-in unit testing framework.
        - [Ultralytics HUB-SDK](https://github.com/ultralytics/hub-sdk): SDK for interacting with Ultralytics HUB.

    Example:
        ```python
        class MyTestCase(TestDatasetSDK):
            def test_something(self):
                self.assertEqual(True, False)
        if __name__ == '__main__':
            unittest.main()
        ```
    """

    def setUp(self):
        """
        Initializes the `HUBClient` instance and performs necessary setup before each unit test.

        Args:
            None

        Returns:
            None

        Notes:
            This method is an override of the `unittest.TestCase.setUp` method. It configures the `HUBClient` instance
            using provided email and password credentials, retrieves a dataset object, and asserts that the `HUBClient`
            instance is correctly initialized.

        References:
            - [unittest.TestCase.setUp](https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp)
        """
        self.client = HUBClient({"email": "<Email>", "password": "<Password>"})  # Add Email Password
        self.dataset = self.client.dataset()
        self.assertIsNotNone(self.client)
        self.assertIsNotNone(self.dataset)

    def test_create_dataset(self):
        """
        Tests dataset creation using HUBClient.

        Args:
            None

        Returns:
            (None): This test does not return a value, it asserts the correct dataset creation.

        Example:
            ```python
            test_instance = TestDatasetSDK()
            test_instance.setUp()
            test_instance.test_create_dataset()
            ```

        References:
            - [unittest documentation](https://docs.python.org/3/library/unittest.html)
            - [HUBClient SDK documentation](https://hub.ultralytics.com)
        """
        data = {"meta": {"name": "my dataset"}, "filename": "example.pt"}
        expected_result = None
        result = self.dataset.create_dataset(data)
        self.assertEqual(result, expected_result)
        self.assertEqual(result.data.get("meta").get("name"), "my dataset")

    def test_get_dataset_by_id(self):
        """
        Retrieves a dataset by its ID using the HUBClient.

        Args:
            dataset_id (str): The unique identifier for the dataset to retrieve.

        Returns:
            (dict | None): A dictionary containing dataset details if found, otherwise None.

        Example:
            ```python
            dataset_id = "12345"
            dataset_info = self.client.dataset(dataset_id)
            ```
        """
        dataset_id = "<Dataset ID>"  # Add dataset ID
        result = self.client.dataset(dataset_id)
        self.assertEqual(result.id, dataset_id)

    def test_update_dataset(self):
        """
        Tests updating a dataset's information using `HUBClient`.

        Args:
            None

        Returns:
            None

        Notes:
            - Assumes dataset ID and valid credentials are set before running the test.

        Example:
            ```python
            def test_update_dataset(self):
                data = {"meta": {"name": "Ricks Secret Dataset"}}
                project_id = "<Dataset ID>"  # Add dataset ID
                result = self.client.dataset(project_id)
                expected_result = "Ricks Secret Dataset"
                result.update(data)
                update_name = result.data.get("meta").get("name")
                self.assertEqual(update_name, expected_result)
            ```

        References:
            - [Ultralytics HUB SDK](https://github.com/ultralytics/hub-sdk)
        """
        data = {"meta": {"name": "Ricks Secret Dataset"}}
        project_id = "<Dataset ID>"  # Add dataset ID
        result = self.client.dataset(project_id)
        expected_result = "Ricks Secret Dataset"
        result.update(data)
        update_name = result.data.get("meta").get("name")
        self.assertEqual(update_name, expected_result)

    def test_list_datasets(self):
        """
        Tests listing of available datasets using HUBClient.

        Args:
            page_size (int): Number of datasets to list per page.
            public (bool): Whether to list only public datasets.

        Returns:
            (list[dict]): List of datasets, each represented as a dictionary containing dataset attributes.

        Example:
            ```python
            result = self.client.dataset_list(page_size=1, public=True)
            assert isinstance(result, list)
            assert len(result) <= 1
            ```
        """
        result = self.client.dataset_list(page_size=1, public=True)
        self.assertNotEqual(len(result), 0)

    def test_upload_dataset(self):
        """
        Tests dataset upload functionality using HUBClient.

        Args:
            None

        Returns:
            (None): This method does not return any value.

        Notes:
            - Ensure that the dataset ID specified is valid and that the file exists and is accessible before
              executing the test.

        Example:
            ```python
            result = test_upload_dataset()
            ```

        References:
            - [HUBClient documentation](https://example.com/hubclient)
        """
        dataset_id = "<Dataset ID>"  # Add dataset ID
        result = self.client.dataset(dataset_id)
        result.upload_dataset(file="coco8.zip")
        self.assertEqual(result.id, dataset_id)

    def test_get_download_link(self):
        """
        Tests the retrieval of a dataset download link using HUBClient.

        Args:
            dataset_id (str): The unique identifier of the dataset.

        Returns:
            (str): The download link for the specified dataset.

        Example:
            ```python
            dataset_id = "<Dataset ID>"
            download_link = self.client.dataset(dataset_id).get_download_link("archive")
            ```

        Notes:
            The dataset ID must be a valid identifier within the HUBClient context.
        """
        dataset_id = "<Dataset ID>"  # Add dataset ID
        result = self.client.dataset(dataset_id)
        download_link = result.get_download_link("archive")
        self.assertEqual(result.id, dataset_id)
        self.assertTrue(download_link.startswith("http"))

    def test_delete_dataset(self):
        """
        Tests dataset deletion functionality using HUBClient.

        Args:
            None

        Returns:
            (int): Status code indicating the result of the delete operation. Expected result is 200.

        Example:
            ```python
            self.test_delete_dataset()
            ```

        References:
            - [HUBClient Documentation](#)
        """
        dataset_id = "<Dataset ID>"  # Add dataset ID
        result = self.client.dataset(dataset_id)
        deleted = result.delete()
        expected_result = 200
        self.assertEqual(deleted.status_code, expected_result)


if __name__ == "__main__":
    unittest.main()
