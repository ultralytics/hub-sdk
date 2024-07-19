from tests.utils.base_class import BaseClass


class Project(BaseClass):
    """
    A Project class for managing project-related operations via a client.

    Attributes:
        client (object): The client object facilitating API communication.

    Methods:
        get_project_by_id: Retrieves a project by its unique identifier.
        create_new_project: Creates a new project with the provided data.
        is_project_exists: Checks whether a project with a specified ID exists.
        update_project: Updates an existing project with new data.
        get_project_name: Retrieves the name of a project by its ID.
        list_public_projects: Lists public projects with pagination.
        delete_project: Deletes a project by its ID.

    Example:
        ```python
        client = YourClientObject()
        project_manager = Project(client)

        # Create a new project
        project_id = project_manager.create_new_project(data={"name": "New Project"})

        # Check if the project exists
        exists = project_manager.is_project_exists(project_id)

        # Update the project
        if exists:
            project_manager.update_project(project_id, data={"description": "Updated description"})

        # Get project name
        project_name = project_manager.get_project_name(project_id)

        # List public projects
        public_projects = project_manager.list_public_projects()

        # Delete the project
        project_manager.delete_project(project_id)
        ```

    References:
        [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
    """

    def __init__(self, client):
        """
        Initializes the Project with a specified client object.

        Args:
            client (object): A client object instance to associate with the Project instance.

        Returns:
            None

        Example:
            ```python
            client_instance = SomeClient(...)
            project = Project(client_instance)
            ```
        """
        self.client = client

    def get_project_by_id(self, project_id):
        """
        Retrieves a project by its ID.

        Args:
            project_id (str): The ID of the project to retrieve.

        Returns:
            (dict): The project object associated with the given project ID.

        Example:
            ```python
            project = Project(client)
            result = project.get_project_by_id("project_12345")
            ```
        """
        self.delay()
        return self.client.project(project_id)

    def create_new_project(self, data):
        """
        Creates a new project with the provided data.

        Args:
            data (dict): The data required to create the project, typically including project configuration details.

        Returns:
            (str): The ID of the newly created project.

        Example:
            ```python
            data = {"name": "New Project", "description": "Project description", "settings": {}}
            project_id = project.create_new_project(data)
            ```

        References:
            - [Python Dictionary Documentation](https://docs.python.org/3/library/stdtypes.html#dict)
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
            project_id (str): The ID of the project to verify.

        Returns:
            (bool): True if the project exists, False otherwise.

        Example:
            ```python
            project = Project(client)
            exists = project.is_project_exists("12345")
            ```

        Notes:
            Exceptions are caught and logged but no re-throwing occurs.

        References:
            - [Python Exception Handling](https://docs.python.org/3/tutorial/errors.html)
            - [Python Logging Module](https://docs.python.org/3/library/logging.html)
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
            data (dict): The data to update the project with key-value pairs representing the properties to be updated.

        Returns:
            None

        Example:
            ```python
            project_id = '123abc'
            data = {'name': 'Updated Project Name', 'description': 'Updated Description'}
            project.update_project(project_id, data)
            ```
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
            (str): The name of the project.

        Example:
            ```python
            project = Project(client)
            name = project.get_project_name("12345")
            ```

        Notes:
            This method assumes that the project ID provided is valid and that the project exists.

        References:
            [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
        """
        return self.get_project_by_id(project_id).data["meta"]["name"]

    def list_public_projects(self):
        """
        Retrieves a list of public projects.

        Args:
            None

        Returns:
            (list[dict]): A list of public project dictionaries, each containing project details.

        Example:
            ```python
            project_instance = Project(client)
            public_projects = project_instance.list_public_projects()
            ```

        Notes:
            The list is limited to a page size of 10 public projects.

        References:
            [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
        """
        self.delay()
        project_list = self.client.project_list(page_size=10, public=True)
        return project_list.results

    def delete_project(self, project_id):
        """
        Deletes a project based on its ID.

        Args:
            project_id (str): The ID of the project to delete.

        Example:
            ```python
            project_instance = Project(client)
            project_instance.delete_project('project123')
            ```
        """
        project = self.get_project_by_id(project_id)
        self.delay()
        project.delete(hard=True)
