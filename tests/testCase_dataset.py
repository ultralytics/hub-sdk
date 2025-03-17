# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import unittest

from hub_sdk import HUBClient


class TestDatasetSDK(unittest.TestCase):
    """
    Unit tests for dataset-related operations using the HUBClient from the Ultralytics HUB-SDK.

    This test suite validates the functionality of dataset operations including creation, retrieval,
    updating, listing, uploading, downloading, and deletion.

    Attributes:
        client (HUBClient): The authenticated HUB client instance used for API interactions.
        dataset (Dataset): A dataset instance for performing operations.
    """

    def setUp(self):
        """Initialize HUBClient instance and other necessary setup before each test."""
        self.client = HUBClient({"email": "<Email>", "password": "<Password>"})  # Add Email Password
        self.dataset = self.client.dataset()
        self.assertIsNotNone(self.client)
        self.assertIsNotNone(self.dataset)

    def test_create_dataset(self):
        """Test dataset creation using HUBClient."""
        data = {"meta": {"name": "my dataset"}, "filename": "example.pt"}
        expected_result = None
        result = self.dataset.create_dataset(data)
        self.assertEqual(result, expected_result)
        self.assertEqual(result.data.get("meta").get("name"), "my dataset")

    def test_get_dataset_by_id(self):
        """Test retrieval of a dataset by its ID using HUBClient."""
        dataset_id = "<Dataset ID>"  # Add dataset ID
        result = self.client.dataset(dataset_id)
        self.assertEqual(result.id, dataset_id)

    def test_update_dataset(self):
        """Test updating a dataset's information using HUBClient."""
        data = {"meta": {"name": "Ricks Secret Dataset"}}
        project_id = "<Dataset ID>"  # Add dataset ID
        result = self.client.dataset(project_id)
        expected_result = "Ricks Secret Dataset"
        result.update(data)
        update_name = result.data.get("meta").get("name")
        self.assertEqual(update_name, expected_result)

    def test_list_datasets(self):
        """Test listing of available datasets using HUBClient."""
        result = self.client.dataset_list(page_size=1, public=True)
        self.assertNotEqual(len(result), 0)

    def test_upload_dataset(self):
        """Test dataset upload functionality using HUBClient."""
        dataset_id = "<Dataset ID>"  # Add dataset ID
        result = self.client.dataset(dataset_id)
        result.upload_dataset(file="coco8.zip")
        self.assertEqual(result.id, dataset_id)

    def test_get_download_link(self):
        """Test retrieving download link for a dataset using HUBClient."""
        dataset_id = "<Dataset ID>"  # Add dataset ID
        result = self.client.dataset(dataset_id)
        download_link = result.get_download_link("archive")
        self.assertEqual(result.id, dataset_id)
        self.assertTrue(download_link.startswith("http"))

    def test_delete_dataset(self):
        """Test dataset deletion functionality using HUBClient."""
        dataset_id = "<Dataset ID>"  # Add dataset ID
        result = self.client.dataset(dataset_id)
        deleted = result.delete()
        expected_result = 200
        self.assertEqual(deleted.status_code, expected_result)


if __name__ == "__main__":
    unittest.main()
