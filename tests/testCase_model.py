# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import unittest

from hub_sdk import HUBClient


class TestSDK(unittest.TestCase):
    """
    Unit test suite for validating HUBClient's model creation, management, and export functionalities.

    This test suite covers the core functionality of the HUBClient including model creation, data retrieval,
    metrics uploading, model exporting, downloading, and deletion.

    Attributes:
        client (HUBClient): The HUBClient instance used for testing.
        model (Model): A model instance created from the client.
    """

    def setUp(self):
        """Initialize test environment, creating mock HUBClient and model instances."""
        self.client = HUBClient({"email": "<Email>", "password": "Password"})  # Add Email Password
        self.model = self.client.model()
        self.assertIsNotNone(self.client)
        self.assertIsNotNone(self.model)

    def test_create_model(self):
        """Test model creation using HUBClient."""
        data = {
            "meta": {"name": "sdk model"},
            "projectId": "<Project ID>",  # Add Project ID
            "datasetId": "<Dataset ID>",  # Add Dataset ID
            "config": {
                "batchSize": "-1",
                "cache": "ram",
                "device": "name",
                "epochs": "5",
                "imageSize": "640",
                "patience": "5",
            },
        }
        expected_result = None
        result = self.model.create_model(data)
        self.assertEqual(result, expected_result)

    def test_get_model_data(self):
        """Assert that retrieving a model with HUBClient returns the expected model ID."""
        model_id = "<Model ID>"  # Add Model ID
        result = self.client.model(model_id)
        self.assertEqual(result.id, model_id)

    def test_upload_metrics(self):
        """Validate uploading of model metrics to HUBClient and check response status."""
        model_id = "<Model ID>"  # Add Model ID
        data = {
            1: '{"loss/1": 0.5, "accuracy/1": 0.85}',
            2: '{"loss/2": 0.4, "accuracy/2": 0.88}',
            3: '{"loss/3": 0.3, "accuracy/3": 0.90}',
        }
        expected_result = "<Model ID>"  # Add Model ID
        result = self.client.model(model_id)
        response = result.upload_metrics(data)
        self.assertEqual(result.data.get("id"), expected_result)
        self.assertEqual(response.status_code, 200)

    def test_export_model(self):
        """Test exporting a model using HUBClient and check for successful response."""
        model_id = "<Model ID>"  # Add Model ID
        result = self.client.model(model_id)
        response = result.export(format="pyTorch")
        self.assertEqual(response.status_code, 200)
        if response.status_code == 500:
            self.assertTrue("Unhandled server error.")

    def test_get_download_link(self):
        """Test model download link generation and validate the URL format."""
        model_id = "<Model ID>"  # Add Model ID
        result = self.client.model(model_id)
        download_link = result.get_download_link("best")
        print(download_link)
        self.assertEqual(result.id, model_id)
        self.assertTrue(download_link.startswith("http"))

    def test_upload_model(self):
        """Test model upload functionality with specified weights file."""
        model_id = "<Model ID>"  # Add Model ID
        expected_result = "<expected_result>"
        result = self.client.model(model_id)
        result.upload_model(is_best=True, epoch="5", weights="example.pt")
        self.assertEqual(result, expected_result)

    def test_delete_model(self):
        """Test model deletion functionality and verify the response status code."""
        model_id = "<Model ID>"  # Add Model ID
        result = self.client.model(model_id)
        deleted = result.delete()
        expected_result = 200
        self.assertEqual(deleted.status_code, expected_result)


if __name__ == "__main__":
    unittest.main()
