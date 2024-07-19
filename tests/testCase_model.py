# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

import unittest

from hub_sdk import HUBClient


class TestSDK(unittest.TestCase):
    """
    Test suite for validating the functionalities of the HUBClient class in the Ultralytics library.

    This class implements various test cases to ensure that the HUBClient interface operates correctly for model creation,
    data retrieval, metric uploading, and other model management tasks.

    Attributes:
        client (HUBClient): The HUBClient instance used for API interactions.
        model (HUBClient.model): The initialized model instance fetched from HUBClient.

    Methods:
        setUp: Initializes the test environment by setting up mock HUBClient and model instances.
        test_create_model: Tests if a model can be successfully created using the HUBClient.
        test_get_model_data: Asserts that fetching model data returns the correct model information.
        test_upload_metrics: Validates if model metrics can be successfully uploaded to the HUBClient.
        test_export_model: Tests the export functionality of a model, checking the response status.
        test_get_download_link: Tests the download link retrieval for a model and validates the response.
        test_upload_model: Asserts that the model upload functionality works and returns the expected result.
        test_delete_model: Tests the deletion functionality of a model and verifies the response status.

    Notes:
        This test class uses unittest for structuring test cases and assertions.

    References:
        [unittest Documentation](https://docs.python.org/3/library/unittest.html)
        [Ultralytics HUB-SDK](https://github.com/ultralytics/hub-sdk)

    Example:
        ```python
        if __name__ == "__main__":
            unittest.main()
        ```
    """

    def setUp(self):
        """
        Initializes the test environment, creating mock HUBClient and model instances.

        Args:
            None

        Returns:
            None

        Notes:
            This function sets up the necessary components for running tests by instantiating a HUBClient with email and
            password credentials, and then initializing a model instance from this client. It ensures that the client is
            not None, which is essential for subsequent test operations involving the HUBClient and model.

        Example:
            ```python
            class MyTest(TestSDK):
                def test_model_initialization(self):
                    self.setUp()
                    self.assertIsNotNone(self.model)
            ```

        References:
            [unittest documentation](https://docs.python.org/3/library/unittest.html)
        """
        self.client = HUBClient({"email": "<Email>", "password": "Password"})  # Add Email Password
        self.model = self.client.model()
        self.assertIsNotNone(self.client)
        self.assertIsNotNone(self.model)

    def test_create_model(self):
        """
        Tests model creation using HUBClient.

        Args:
            None

        Returns:
            (None): The function does not return any value, but it executes the test case for model creation.

        Example:
            ```python
            test_sdk = TestSDK()
            test_sdk.setUp()
            test_sdk.test_create_model()
            ```

        Notes:
            This function uses hardcoded data for testing the creation of a model, such as meta information,
            project ID, dataset ID, and training configuration options. Ensure the placeholders like
            `<Email>`, `<Password>`, `<Project ID>`, and `<Dataset ID>` are correctly replaced with actual values
            before running the test.

        References:
            [HUBClient Documentation](https://example.com/HUBClient-doc)
        """
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
        """
        Gets model data from the HUBClient based on the provided model ID.

        Args:
            model_id (str): Unique identifier for the model.

        Returns:
            (dict | None): Dictionary containing the model data if it exists, otherwise None.

        Example:
            ```python
            model_id = "sample_model_id"
            model_data = test_get_model_data(model_id)
            ```

        References:
            - [Ultralytics HUB-SDK](https://github.com/ultralytics/hub-sdk) - Official GitHub repository for the Ultralytics HUB-SDK.
        """
        model_id = "<Model ID>"  # Add Model ID
        result = self.client.model(model_id)
        self.assertEqual(result.id, model_id)

    def test_upload_metrics(self):
        """
        Validates uploading of model metrics to HUBClient.

        Args:
            model_id (str): The unique identifier of the model.
            data (dict): A dictionary where keys are epoch numbers and values are JSON strings containing
                metric names and their corresponding values for each epoch.

        Returns:
            (str | None): The model ID if metrics are successfully uploaded, otherwise None.

        Example:
            ```python
            model_id = "123456"
            metrics = {
                1: '{"loss/1": 0.5, "accuracy/1": 0.85}',
                2: '{"loss/2": 0.4, "accuracy/2": 0.88}',
                3: '{"loss/3": 0.3, "accuracy/3": 0.90}',
            }
            response = test_upload_metrics(model_id, metrics)
            ```

        References:
            - [HUBClient Documentation](https://example.com/hubclient-docs)
        """
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
        """
        Tests exporting a model using HUBClient and checks for successful response.

        Args:
            None

        Returns:
            (None): This function does not return any value.

        Notes:
            This function primarily performs unit testing on the model export functionality using the HUBClient
            interface within the Ultralytics SDK.

        Example:
            ```python
            test_sdk = TestSDK()
            test_sdk.setUp()
            test_sdk.test_export_model()
            ```

        References:
            - [PyTorch](https://pytorch.org/)
            - [Unit Testing in Python](https://docs.python.org/3/library/unittest.html)
        """
        model_id = "<Model ID>"  # Add Model ID
        result = self.client.model(model_id)
        response = result.export(format="pyTorch")
        self.assertEqual(response.status_code, 200)
        if response.status_code == 500:
            self.assertTrue("Unhandled server error.")

    def test_get_download_link(self):
        """
        Tests model download functionality and validates the response status code.

        Args:
            None

        Returns:
            None

        Notes:
            Ensure that the `model_id` is correctly specified and the HUBClient's model object supports the
            `get_download_link` method for accurate functionality.

            The method prints the download link to the standard output and asserts that the model ID matches the
            expected `model_id`.

        Example:
            ```python
            def test_get_download_link(self):
                model_id = "<Model ID>"  # Add Model ID
                result = self.client.model(model_id)
                download_link = result.get_download_link("best")
                print(download_link)
                self.assertEqual(result.id, model_id)
            ```

        References:
            - [HUBClient Documentation](https://sdk.ultralytics.com/hubclient.html)
        """
        model_id = "<Model ID>"  # Add Model ID
        result = self.client.model(model_id)
        download_link = result.get_download_link("best")
        print(download_link)
        self.assertEqual(result.id, model_id)
        self.assertTrue(download_link.startswith("http"))

    def test_upload_model(self):
        """
        Asserts that model metrics are uploaded and returns correct status code.

        Args:
            None

        Returns:
            (None): This test function does not return any value but asserts the outcomes using unittest methods.

        Example:
            ```python
            class TestSDK(unittest.TestCase):
                ...
                def test_upload_model(self):
                    model_id = "<Model ID>"
                    expected_result = "<expected_result>"
                    result = self.client.model(model_id)
                    result.upload_model(is_best=True, epoch="5", weights="example.pt")
            ```
        """
        model_id = "<Model ID>"  # Add Model ID
        expected_result = "<expected_result>"
        result = self.client.model(model_id)
        result.upload_model(is_best=True, epoch="5", weights="example.pt")
        self.assertEqual(result, expected_result)

    def test_delete_model(self):
        """
        Tests model delete functionality and asserts the expected result matches.

        Args:
            None

        Returns:
            (None)

        Example:
            ```python
            test_instance = TestSDK()
            test_instance.test_delete_model()
            ```

        Notes:
            This function makes assertions using the unittest framework to ensure that the delete functionality of
            the HUBClient model works as expected.
        """
        model_id = "<Model ID>"  # Add Model ID
        result = self.client.model(model_id)
        deleted = result.delete()
        expected_result = 200
        self.assertEqual(deleted.status_code, expected_result)


if __name__ == "__main__":
    unittest.main()
