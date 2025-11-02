# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from tests.utils.base_class import BaseClass


class Project(BaseClass):
    """
    Manages project operations such as creation, retrieval, updating, and deletion.

    This class provides methods to interact with projects through a client interface, allowing for operations like
    creating new projects, retrieving existing ones, checking existence, updating, and deleting projects.

    Attributes:
        client (Any): The client object used to interact with the project API.

    Methods:
        get_project_by_id: Retrieve a project by its ID.
        create_new_project: Create a new project with provided data.
        is_project_exists: Check if a project with specified ID exists.
        update_project: Update an existing project with new data.
        get_project_name: Get the name of a project by its ID.
        list_public_projects: Get a list of public projects.
        delete_project: Delete a project by its ID.
    """

    def __init__(self, client):
        """Initialize the Project with a specified client object."""
        self.client = client

    def get_project_by_id(self, project_id):
        """
        Retrieve a project by its ID.

        Args:
            project_id (str): The ID of the project to retrieve.

        Returns:
            (Any): The project object associated with the given project ID.
        """
        self.delay()
        return self.client.project(project_id)

    def create_new_project(self, data):
        """
        Create a new project with the provided data.

        Args:
            data (dict): The data to create the project.

        Returns:
            (str): The ID of the newly created project.
        """
        self.delay()
        project = self.client.project()
        self.delay()
        project.create_project(data)
        return project.id

    def is_project_exists(self, project_id):
        """
        Check if a project with the specified ID exists.

        Args:
            project_id (str): The ID of the project.

        Returns:
            (bool): True if the project exists, False otherwise.
        """
        try:
            project = self.get_project_by_id(project_id)
            return bool(project.data)
        except Exception as e:
            log = self.get_logger()
            log.error(e)
            return False

    def update_project(self, project_id, data):
        """
        Update an existing project with the provided data.

        Args:
            project_id (str): The ID of the project to update.
            data (dict): The data to update the project.
        """
        project = self.get_project_by_id(project_id)
        self.delay()
        project.update(data)

    def get_project_name(self, project_id):
        """
        Retrieve the name of a project based on its ID.

        Args:
            project_id (str): The ID of the project.

        Returns:
            (str): The name of the project.
        """
        return self.get_project_by_id(project_id).data["meta"]["name"]

    def list_public_projects(self):
        """
        Retrieve a list of public projects.

        Returns:
            (List): A list of public projects, limited to a page size of 10.
        """
        self.delay()
        project_list = self.client.project_list(page_size=10, public=True)
        return project_list.results

    def delete_project(self, project_id):
        """
        Delete a project based on its ID.

        Args:
            project_id (str): The ID of the project to delete.
        """
        project = self.get_project_by_id(project_id)
        self.delay()
        project.delete(hard=True)
