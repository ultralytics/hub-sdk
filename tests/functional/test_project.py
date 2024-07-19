import pytest

from tests.features.object_manager import ObjectManager
from tests.test_data.data import TestData
from tests.utils.base_class import BaseClass


class TestProject(BaseClass):
    """
    TestProject class for testing project-related operations in a project management system.

    The TestProject class contains methods that test various functionalities related to project management, such as
    retrieving, creating, updating, deleting, and listing projects within a system. The tests utilize pytest for
    test execution and assertion, ensuring that project operations perform as expected.

    Attributes:
        client (any): The client used to interface with the project management system, inherited from BaseClass.

    Methods:
        test_project_001: Verifies the successful retrieval of a project by its ID.
        test_project_002: Verifies the successful creation of a new project.
        test_project_003: Verifies the successful update of project metadata.
        test_project_004: Verifies the successful deletion of a project.
        test_project_005: Verifies the successful listing of public projects.

    Example:
        ```python
        class TestProjectUsage(BaseClass):
            @pytest.mark.smoke
            def test_project_operations(self):
                test_project = TestProject()
                test_project.test_project_001()
                test_project.test_project_002()
        ```

    References:
        [pytest documentation](https://docs.pytest.org/en/latest/)
        [Project Management Systems](https://en.wikipedia.org/wiki/Project_management)
    """

    @pytest.mark.smoke
    def test_project_001(self):
        """
        Verify successful retrieval of a project by ID.

        Args:
            No arguments are required for this function.

        Returns:
            None: This function does not return any value. It uses assertions to validate the test outcome.

        Example:
            ```python
            def setup_method(self):
                self.test_instance = TestProject()

            def test_example(self):
                self.test_instance.test_project_001()
            ```

        Notes:
            - This test case retrieves a project using a valid project ID and verifies its retrieval successfully.
            - Logs pertinent information during execution for debugging purposes.

        References:
            [pytest documentation](https://docs.pytest.org/)
        """

        log = self.get_logger()
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
        """
        Verifies successful creation of a new project.

        Args:
            request (CustomRequest): The pytest request object, which provides information about the executing
                test function.
            delete_test_project (function): A fixture function that handles the deletion of the test project for
                cleanup.

        Returns:
            None

        Notes:
            This function relies on external test data and the `ObjectManager` utility to create and manage
            project entities within the test environment. Project creation and retrieval are logged for
            verification purposes.

        References:
            [PyTest Documentation](https://docs.pytest.org/en/stable/)
            [GetLogger Method](https://docs.python.org/3/library/logging.html#logging.getLogger)
        """

        log = self.get_logger()

        new_project_data = TestData().get_projects_data()["new_project_data"]
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
    def test_project_003(self, request, create_test_project, delete_test_project):
        """
        Verifies successful update of project metadata.

        Args:
            request (FixtureRequest): The request fixture for accessing test details and context.
            create_test_project (Fixture): Fixture to create a test project before running the test.
            delete_test_project (Fixture): Fixture to delete the test project after running the test.

        Returns:
            (None): This function does not return anything.

        Example:
            ```python
            request = ...  # acquired from pytest fixtures
            create_test_project = ...  # acquired from pytest fixtures
            delete_test_project = ...  # acquired from pytest fixtures

            TestProject().test_project_003(request, create_test_project, delete_test_project)
            ```

        Notes:
            This function relies on several pytest fixtures for setup and teardown, and thus is intended to
            be executed within a pytest environment.

        References:
            - [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
            - [Pytest Documentation](https://docs.pytest.org/en/stable/)
        """

        log = self.get_logger()

        # Retrieve necessary data
        test_name = request.node.name
        project_id_key = f"project_id_for_{test_name}"
        project_id = request.config.cache.get(project_id_key, None)
        desired_project_data = TestData().get_projects_data()["desired_project_data"]
        desired_project_name = desired_project_data["meta"]["name"]

        log.info(
            f"Attempting to update metadata for project with ID {project_id}. Desired project data: "
            f"{desired_project_name}"
        )

        object_manager = ObjectManager(self.client)
        project_obj = object_manager.get_project()

        # Update project metadata
        project_obj.update_project(project_id, desired_project_data)

        log.info("Project metadata updated successfully.")

        # Get the updated project name
        updated_project_name = project_obj.get_project_name(project_id)

        log.info(f"Updated project name: {updated_project_name}")

        assert (
            updated_project_name == desired_project_name
        ), f"Project name is not updated as expected. Actual: {updated_project_name}, Expected: {desired_project_name}"

    @pytest.mark.smoke
    def test_project_004(self, request, create_test_project):
        """
        Verify successful deletion of a project.

        Args:
            request (pytest.FixtureRequest): The pytest request object for accessing test context and state.
            create_test_project (fixture): A fixture that ensures a test project exists before performing the test.

        Returns:
            (None): This function does not return a value.

        Example:
            ```python
            def test_project_004(self, request, create_test_project):
                self.test_project_004(request, create_test_project)
            ```

        Notes:
            This function is marked with the `@pytest.mark.smoke` decorator to indicate it's a smoke test.
        """

        log = self.get_logger()

        # Retrieve necessary data
        test_name = request.node.name
        project_id_key = f"project_id_for_{test_name}"
        project_id = request.config.cache.get(project_id_key, None)

        log.info(f"Attempting to delete project with ID: {project_id}")

        object_manager = ObjectManager(self.client)
        project_obj = object_manager.get_project()

        # Delete the project
        project_obj.delete_project(project_id)

        log.info("Project deleted successfully.")

        # Verify if the project no longer exists
        assert not project_obj.is_project_exists(
            project_id
        ), f"Project with ID {project_id} still exists after deletion."

    @pytest.mark.smoke
    def test_project_005(self):
        """
        Verifies successful listing of public projects.

        Returns:
            (list[dict]): List of public project information; each dictionary contains project details like id,
                name, and metadata.

        Example:
            ```python
            def test_project_005():
                project_list = self.test_project_005()
                first_project = project_list[0]
                assert "id" in first_project
            ```
        """

        log = self.get_logger()

        log.info("Attempting to list public projects.")

        object_manager = ObjectManager(self.client)
        project_obj = object_manager.get_project()

        # List public projects
        public_project_list = project_obj.list_public_projects()

        log.info(f"Public projects listed successfully. First dataset information: {public_project_list[0]}")

        assert "id" in public_project_list[0], "ID information not found in the project data"
        assert "meta" in public_project_list[0], "Meta information not found in the project data"
