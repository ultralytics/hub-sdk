# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

import unittest

from hub_sdk import HUBClient


class TestProjectSDK(unittest.TestCase):
    """
    A TestProjectSDK class for testing project-related functionalities using the Ultralytics HUB SDK.

    This class provides methods to test the creation, retrieval, updating, listing, and deletion of projects, as well as
    the upload of images to a project. It uses the HUBClient to interact with the Ultralytics HUB.

    Attributes:
        client (HUBClient): An instance of the HUBClient for interacting with the Ultralytics HUB.
        project (Project): A project instance retrieved using the HUBClient.

    Methods:
        setUp: Initializes the test environment and instances of HUBClient before each test.
        test_create_project: Tests project creation functionality using the HUBClient.
        test_get_project_by_id: Tests the retrieval of a project by its ID using the HUBClient.
        test_update_project: Tests updating a project's details using the HUBClient.
        test_list_projects: Tests listing all projects using the HUBClient.
        test_upload_image: Tests the image upload functionality to a project using the HUBClient.
        test_delete_project: Tests the deletion of a project using the HUBClient.

    Example:
        ```python
        class MyTestCase(TestProjectSDK):
            def runTest(self):
                self.test_create_project()
                self.test_get_project_by_id()
                self.test_update_project()
                self.test_list_projects()
                self.test_upload_image()
                self.test_delete_project()
        ```

    References:
        - [HUBClient Documentation](https://example.com/hub_sdk_docs)
    """

    def setUp(self):
        """
        Initializes test environment and instances of HUBClient before each test.

        Args:
            None

        Returns:
            None

        Example:
            ```python
            import unittest
            from hub_sdk import HUBClient

            class TestProjectSDK(unittest.TestCase):
                def setUp(self):
                    self.client = HUBClient({"email": "<Email>", "password": "<Password>"})
                    self.project = self.client.project()
                    self.assertIsNotNone(self.client)
            ```

        Notes:
            - Ensure to replace "<Email>" and "<Password>" with valid credentials for HUBClient initialization.
        """
        self.client = HUBClient({"email": "<Email>", "password": "<Password>"})  # Add Email Password
        self.project = self.client.project()
        self.assertIsNotNone(self.client)
        self.assertIsNotNone(self.project)

    def test_create_project(self):
        """
        Tests project creation using HUBClient.

        Args:
            data (dict): Data dictionary containing metadata for project creation, e.g., {"meta": {"name": "my project"}}.

        Returns:
            (None): This method does not return a value.

        Example:
            ```python
            self.client = HUBClient({"email": "test@example.com", "password": "password"})
            self.project = self.client.project()
            data = {"meta": {"name": "my project"}}
            expected_result = None
            result = self.project.create_project(data)
            self.assertEqual(result, expected_result)
            ```

        Notes:
            Ensure the HUBClient has correct authentication details before running the test.

        References:
            - [HUBClient SDK Documentation](https://example.com/hub-client-sdk-docs)
        """
        data = {"meta": {"name": "my project"}}
        expected_result = None
        result = self.project.create_project(data)
        self.assertEqual(result, expected_result)
        self.assertEqual(result.data.get("meta").get("name"), "my project")

    def test_get_project_by_id(self):
        """
        Tests retrieval of a project by its ID using HUBClient.

        Args:
            project_id (str): Unique identifier of the project to be retrieved.

        Returns:
            (dict): Project details as a dictionary containing meta-information and other relevant fields.

        Example:
            ```python
            project_id = "123456"
            project_details = self.client.project(project_id)
            ```

        References:
            [Ultralytics HUB SDK Documentation](https://example.com/hub-sdk-docs)
        """
        project_id = "<Project ID>"  # Add Project ID
        result = self.client.project(project_id)
        self.assertEqual(result.id, project_id)

    def test_update_project(self):
        """
        Tests updating a project's details using HUBClient.

        Args:
            None

        Returns:
            None

        Notes:
            This test checks the functionality of the `update` method in HUBClient by updating the project's
            metadata and verifying the update.

        Example:
            ```python
            project_id = "<Project ID>"
            data = {"meta": {"name": "Project name update"}}
            result = self.client.project(project_id)
            result.update(data)
            ```
        """
        data = {"meta": {"name": "Project name update"}}
        project_id = "<Project ID>"  # Add Project ID
        result = self.client.project(project_id)
        expected_result = "Project name update"
        result.update(data)
        self.assertEqual(result.data.get("meta").get("name"), expected_result)

    def test_list_projects(self):
        """
        Tests listing of all projects using HUBClient.

        Args:
            page_size (int): The number of projects to list per page.
            public (bool): Flag to filter public projects.

        Returns:
            (list[dict]): A list of project details, where each project is represented by a dictionary.

        Example:
            ```python
            result = self.client.project_list(page_size=1, public=True)
            ```

        References:
            - [HUBClient API Documentation](https://github.com/ultralytics/hub-sdk)
        """
        result = self.client.project_list(page_size=1, public=True)
        self.assertNotEqual(len(result), 0)

    def test_upload_image(self):
        """
        Tests image upload functionality using HUBClient.

        Args:
            None

        Returns:
            None

        Example:
            ```python
            test_sdk = TestProjectSDK()
            test_sdk.setUp()
            test_sdk.test_upload_image()
            ```

        Notes:
            Ensure the 'project_id' variable is set to a valid project ID and 'file' is set to a valid image file path before
            running the test.

        References:
            [HUBClient Documentation](https://example.com/hub-client-docs)
        """
        project_id = "<Project ID>"  # Add Project ID
        result = self.client.project(project_id)
        result.upload_image(file="project_image.jpeg")
        self.assertEqual(result.id, project_id)

    def test_delete_project(self):
        """
        Deletes a project using HUBClient.

        Args:
            project_id (str): The unique identifier of the project to be deleted.

        Returns:
            (int): HTTP status code representing the result of the deletion operation.

        Example:
            ```python
            project_id = "12345"
            result = self.client.project(project_id).delete()
            assert result == 200
            ```

        Notes:
            Ensure the `project_id` is valid and the user has the necessary permissions to delete the project.

        References:
            - [HUBClient Documentation](https://hub-sdk-docs.example.com)
            - [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
        """
        project_id = "<Project ID>"  # Add Project ID
        result = self.client.project(project_id)
        deleted = result.delete()
        expected_result = 200
        self.assertEqual(deleted.status_code, expected_result)


if __name__ == "__main__":
    unittest.main()
