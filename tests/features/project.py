# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from tests.utils.base_class import BaseClass


class Project(BaseClass):
    """Manages project operations such as creation, retrieval, updating, and deletion."""

    def __init__(self, client):
        """Initialize the Project with a specified client object."""
        self.client = client

    def get_project_by_id(self, project_id):
        """
        Retrieves a project by its ID.

        Args:
            project_id (str): The ID of the project to retrieve.

        Returns:
            The project object associated with the given project ID.
        """
        self.delay()
        return self.client.project(project_id)

    def create_new_project(self, data):
        """
        Creates a new project with the provided data.

        Args:
            data (dict): The data to create the project.

        Returns:
            str: The ID of the newly created project.
        """
        self.delay()
        project = self.client.project()
        self.delay()
        project.create_project(data)
        return project.id

    def is_project_exists(self, project_id):
        """
        Checks if a project with the specified ID exists.

        Args:
            project_id (str): The ID of the project.

        Returns:
            bool: True if the project exists, False otherwise.
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
        Updates an existing project with the provided data.

        Args:
            project_id (str): The ID of the project to update.
            data (dict): The data to update the project.
        """
        project = self.get_project_by_id(project_id)
        self.delay()
        project.update(data)

    def get_project_name(self, project_id):
        """
        Retrieves the name of a project based on its ID.

        Args:
            project_id (str): The ID of the project.

        Returns:
            str: The name of the project.
        """
        return self.get_project_by_id(project_id).data["meta"]["name"]

    def list_public_projects(self):
        """
        Retrieves a list of public projects.

        Returns:
            list: A list of public projects, limited to a page size of 10.
        """
        self.delay()
        project_list = self.client.project_list(page_size=10, public=True)
        return project_list.results

    def delete_project(self, project_id):
        """
        Deletes a project based on its ID.

        Args:
            project_id (str): The ID of the project to delete.
        """
        project = self.get_project_by_id(project_id)
        self.delay()
        project.delete(hard=True)
