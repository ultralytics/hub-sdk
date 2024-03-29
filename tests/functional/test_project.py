import pytest
from tests.features.object_manager import ObjectManager
from tests.test_data.data import TestData
from tests.utils.base_class import BaseClass


class TestProject(BaseClass):
    @pytest.mark.smoke
    def test_project_001(self):
        """Verify successful retrieval of a project by ID"""

        log = self.getLogger()
        project_id = TestData().get_projects_data()["valid_project_ID"]
        log.info(f"Attempting to retrieve project with ID: {project_id}")

        object_manager = ObjectManager(self.client)
        project_obj = object_manager.get_project()
        project = project_obj.get_project_by_id(project_id)

        log.info(f"Project retrieved successfully. Project data: {project.data}")

        assert "id" in project.data, "ID information not found in the project data"
        assert "meta" in project.data, "Meta information not found in the project data"

    @pytest.mark.smoke
    def test_project_002(self, request, delete_test_project):
        """Verify successful creation of a new project"""

        log = self.getLogger()

        new_project_data = TestData().get_projects_data()['new_project_data']
        log.info(f"Attempting to create a new project with data: {new_project_data}")

        object_manager = ObjectManager(self.client)
        project_obj = object_manager.get_project()

        # Create new project
        project_id = project_obj.create_new_project(new_project_data)

        log.info(f"New project created successfully. Project ID: {project_id}")

        # Set the project_id in the cache with a key that includes the test name
        test_name = request.node.name
        project_id_key = f"project_id_for_test_{test_name}"
        request.config.cache.set(project_id_key, project_id)

        assert project_obj.is_project_exists(project_id)

    @pytest.mark.smoke
    def test_project_003(self,  request, create_test_project, delete_test_project):
        """Verify successful update of project metadata"""

        log = self.getLogger()

        # Retrieve necessary data
        test_name = request.node.name
        project_id_key = f"project_id_for_{test_name}"
        project_id = request.config.cache.get(project_id_key, None)
        desired_project_data = TestData().get_projects_data()['desired_project_data']
        desired_project_name = desired_project_data['meta']['name']

        log.info(
            f"Attempting to update metadata for project with ID {project_id}. Desired project data: "
            f"{desired_project_name}")

        object_manager = ObjectManager(self.client)
        project_obj = object_manager.get_project()

        # Update project metadata
        project_obj.update_project(project_id, desired_project_data)

        log.info(f"Project metadata updated successfully.")

        # Get the updated project name
        updated_project_name = project_obj.get_project_name(project_id)

        log.info(f"Updated project name: {updated_project_name}")

        assert updated_project_name == desired_project_name, \
            f"Project name is not updated as expected. Actual: {updated_project_name}, Expected: {desired_project_name}"

    @pytest.mark.smoke
    def test_project_004(self, request, create_test_project):
        """Verify successful deletion of a project"""

        log = self.getLogger()

        # Retrieve necessary data
        test_name = request.node.name
        project_id_key = f"project_id_for_{test_name}"
        project_id = request.config.cache.get(project_id_key, None)

        log.info(f"Attempting to delete project with ID: {project_id}")

        object_manager = ObjectManager(self.client)
        project_obj = object_manager.get_project()

        # Delete the project
        project_obj.delete_project(project_id)

        log.info(f"Project deleted successfully.")

        # Verify if the project no longer exists
        assert not project_obj.is_project_exists(
            project_id), f"Project with ID {project_id} still exists after deletion."

    @pytest.mark.smoke
    def test_project_005(self):
        """Verify successful listing of public projects"""

        log = self.getLogger()

        log.info("Attempting to list public projects.")

        object_manager = ObjectManager(self.client)
        project_obj = object_manager.get_project()

        # List public projects
        public_project_list = project_obj.list_public_projects()

        log.info(f"Public projects listed successfully. First dataset information: {public_project_list[0]}")

        assert "id" in public_project_list[0], "ID information not found in the project data"
        assert "meta" in public_project_list[0], "Meta information not found in the project data"
