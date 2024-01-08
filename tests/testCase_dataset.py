import unittest

from hub_sdk import HUBClient


class TestDatasetSDK(unittest.TestCase):
    def setUp(self):
        self.client = HUBClient({"email": "<Email>", "password": "<Password>"})  # Add Email Password
        self.dataset = self.client.dataset()
        self.assertIsNotNone(self.client)
        self.assertIsNotNone(self.dataset)

    def test_create_dataset(self):
        data = {"meta": {"name": "my dataset"}, "filename": "example.pt"}
        expected_result = None
        result = self.dataset.create_dataset(data)
        self.assertEqual(result, expected_result)
        self.assertEqual(result.data.get("meta").get("name"), "my dataset")

    def test_get_dataset_by_id(self):
        dataset_id = "<Dataset ID>"  # Add dataset ID
        result = self.client.dataset(dataset_id)
        self.assertEqual(result.id, dataset_id)

    def test_update_dataset(self):
        data = {"meta": {"name": "Ricks Secret Dataset"}}
        project_id = "<Dataset ID>"  # Add dataset ID
        result = self.client.dataset(project_id)
        expected_result = "Ricks Secret Dataset"
        result.update(data)
        update_name = result.data.get("meta").get("name")
        self.assertEqual(update_name, expected_result)

    def test_list_datasets(self):
        result = self.client.dataset_list(page_size=1, public=True)
        self.assertNotEqual(len(result), 0)

    def test_upload_dataset(self):
        dataset_id = "<Dataset ID>"  # Add dataset ID
        result = self.client.dataset(dataset_id)
        result.upload_dataset(file="coco8.zip")
        self.assertEqual(result.id, dataset_id)

    def test_get_download_link(self):
        dataset_id = "<Dataset ID>"  # Add dataset ID
        result = self.client.dataset(dataset_id)
        download_link = result.get_download_link("archive")
        self.assertEqual(result.id, dataset_id)
        self.assertTrue(download_link.startswith("http"))

    def test_delete_dataset(self):
        dataset_id = "<Dataset ID>"  # Add dataset ID
        result = self.client.dataset(dataset_id)
        deleted = result.delete()
        expected_result = 200
        self.assertEqual(deleted.status_code, expected_result)


if __name__ == "__main__":
    unittest.main()
