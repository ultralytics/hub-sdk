# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import unittest

from hub_sdk import HUBClient


class TestProjectSDK(unittest.TestCase):
    """
    Unit test suite for verifying project functionalities in HUBClient.

    This test suite validates the core project operations available through the HUBClient,
    including creation, retrieval, updating, listing, image upload, and deletion of projects.

    Attributes:
        client (HUBClient): An authenticated instance of the HUBClient.
        project (Project): A project instance from the HUBClient.
    """

    def setUp(self):
        """Initialize test environment with HUBClient instance before each test."""
        self.client = HUBClient({"email": "<Email>", "password": "<Password>"})  # Add Email Password
        self.project = self.client.project()
        self.assertIsNotNone(self.client)
        self.assertIsNotNone(self.project)

    def test_create_project(self):
        """Tests project creation using HUBClient."""
        data = {"meta": {"name": "my project"}}
        expected_result = None
        result = self.project.create_project(data)
        self.assertEqual(result, expected_result)
        self.assertEqual(result.data.get("meta").get("name"), "my project")

    def test_get_project_by_id(self):
        """Tests retrieval of a project by its ID using HUBClient."""
        project_id = "<Project ID>"  # Add Project ID
        result = self.client.project(project_id)
        self.assertEqual(result.id, project_id)

    def test_update_project(self):
        """Tests updating a project's details using HUBClient."""
        data = {"meta": {"name": "Project name update"}}
        project_id = "<Project ID>"  # Add Project ID
        result = self.client.project(project_id)
        expected_result = "Project name update"
        result.update(data)
        self.assertEqual(result.data.get("meta").get("name"), expected_result)

    def test_list_projects(self):
        """Tests listing of all projects using HUBClient."""
        result = self.client.project_list(page_size=1, public=True)
        self.assertNotEqual(len(result), 0)

    def test_upload_image(self):
        """Tests image upload functionality using HUBClient."""
        project_id = "<Project ID>"  # Add Project ID
        result = self.client.project(project_id)
        result.upload_image(file="project_image.jpeg")
        self.assertEqual(result.id, project_id)

    def test_delete_project(self):
        """Tests deletion of a project using HUBClient."""
        project_id = "<Project ID>"  # Add Project ID
        result = self.client.project(project_id)
        deleted = result.delete()
        expected_result = 200
        self.assertEqual(deleted.status_code, expected_result)


if __name__ == "__main__":
    unittest.main()
