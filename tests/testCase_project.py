import unittest

from hub_sdk import HUBClient


class TestProjectSDK(unittest.TestCase):
    def setUp(self):
        self.client = HUBClient({"email": "<Email>", "password": "<Password>"})  # Add Email Password
        self.project = self.client.project()
        self.assertIsNotNone(self.client)
        self.assertIsNotNone(self.project)

    def test_create_project(self):
        data = {"meta": {"name": "my project"}}
        expected_result = None
        result = self.project.create_project(data)
        self.assertEqual(result, expected_result)
        self.assertEqual(result.data.get("meta").get("name"), "my project")

    def test_get_project_by_id(self):
        project_id = "<Project ID>"  # Add Project ID
        result = self.client.project(project_id)
        self.assertEqual(result.id, project_id)

    def test_update_project(self):
        data = {"meta": {"name": "Project name update"}}
        project_id = "<Project ID>"  # Add Project ID
        result = self.client.project(project_id)
        expected_result = "Project name update"
        result.update(data)
        self.assertEqual(result.data.get("meta").get("name"), expected_result)

    def test_list_projects(self):
        result = self.client.project_list(page_size=1, public=True)
        self.assertNotEqual(len(result), 0)

    def test_upload_image(self):
        project_id = "<Project ID>"  # Add Project ID
        result = self.client.project(project_id)
        result.upload_image(file="project_image.jpeg")
        self.assertEqual(result.id, project_id)

    def test_delete_project(self):
        project_id = "<Project ID>"  # Add Project ID
        result = self.client.project(project_id)
        deleted = result.delete()
        expected_result = 200
        self.assertEqual(deleted.status_code, expected_result)


if __name__ == "__main__":
    unittest.main()
