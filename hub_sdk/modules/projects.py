# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

from typing import Any, Dict, Optional

from requests import Response

from hub_sdk.base.crud_client import CRUDClient
from hub_sdk.base.paginated_list import PaginatedList
from hub_sdk.base.server_clients import ProjectUpload


class Projects(CRUDClient):
    """
    A class for interacting with Projects through CRUD operations, extending CRUDClient with project-specific methods.

    Attributes:
        hub_client (ProjectUpload): Instance for managing model uploads.
        id (str | None): Unique project identifier.
        data (dict): Dictionary storing project information.

    Methods:
        get_data: Retrieves and stores project details.
        create_project: Creates a new project and sets its ID.
        delete: Deletes the project, optionally hard (permanent).
        update: Updates project information.
        upload_image: Uploads an image associated with the project.

    Example:
        ```python
        projects = Projects(project_id='12345')
        projects.get_data()
        projects.create_project({'name': 'New Project'})
        projects.update({'description': 'Updated description'})
        response = projects.upload_image('path/to/image.jpg')
        ```

    References:
        [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
    """

    def __init__(self, project_id: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        """
        Initializes a Projects object for CRUD operations on project data.

        Args:
            project_id (str | None): The unique identifier of the project to retrieve data for, if available.
            headers (dict[str, Any] | None): A dictionary of HTTP headers to be included in API requests, for
                authentication and other settings.

        Returns:
            None

        Notes:
            This class extends CRUDClient and sets up an instance of ProjectUpload for model uploads. The 'id'
            attribute is set during initialization and can be used to uniquely identify a project. The 'data'
            attribute stores project data fetched from the API.

        References:
            - [Requests Library](https://docs.python-requests.org/en/master/)
            - [Extending Classes in Python](https://docs.python.org/3/tutorial/classes.html#inheritance)
        """
        super().__init__("projects", "project", headers)
        self.hub_client = ProjectUpload(headers)
        self.id = project_id
        self.data = {}
        if project_id:
            self.get_data()

    def get_data(self) -> None:
        """
        Retrieves data for the current project instance.

        Sends a request to fetch and store project data if a valid project ID is set; otherwise, logs an error.

        Args:
            None

        Returns:
            (None): The method does not return a value.

        Example:
            ```python
            project = Projects(project_id="12345")
            project.get_data()
            ```
        """
        if not self.id:
            self.logger.error("No project id has been set. Update the project id or create a project.")
            return

        try:
            response = super().read(self.id)

            if response is None:
                self.logger.error(f"Received no response from the server for project ID: {self.id}")
                return

            # Check if the response has a .json() method (it should if it's a response object)
            if not hasattr(response, "json"):
                self.logger.error(f"Invalid response object received for project ID: {self.id}")
                return

            resp_data = response.json()
            if resp_data is None:
                self.logger.error(f"No data received in the response for project ID: {self.id}")
                return

            self.data = resp_data.get("data", {})
            self.logger.debug(f"Project data retrieved for id ID: {self.id}")

        except Exception as e:
            self.logger.error(f"An error occurred while retrieving data for project ID: {self.id}, {e}")

    def create_project(self, project_data: dict) -> None:
        """
        Creates a new project with the provided data and sets the project ID for the current instance.

        Args:
            project_data (dict): A dictionary containing the data for creating the project.

        Returns:
            (None): The method does not return a value.

        Example:
            ```python
            project_data = {
                "name": "New Project",
                "description": "A detailed description of the new project."
            }
            project_instance = Projects()
            project_instance.create_project(project_data)
            ```
        """
        resp = super().create(project_data).json()
        self.id = resp.get("data", {}).get("id")
        self.get_data()

    def delete(self, hard: Optional[bool] = False) -> Optional[Response]:
        """
        Delete the project resource represented by this instance.

        Args:
            hard (bool, optional): If True, perform a hard (permanent) delete.

        Note:
            The 'hard' parameter determines whether to perform a soft delete (default) or a hard delete.
            In a soft delete, the project might be marked as deleted but retained in the system. In a hard delete, the
            project is permanently removed from the system.

        Returns:
            (Optional[Response]): Response object from the delete request, or None if delete fails.

        References:
            [requests.Response Documentation](https://docs.python-requests.org/en/master/api/#requests.Response)
        """
        return super().delete(self.id, hard)

    def update(self, data: dict) -> Optional[Response]:
        """
        Update the project resource represented by this instance.

        Args:
            data (dict): The updated data for the project resource.

        Returns:
            (Optional[Response]): Response object from the update request, or None if the update fails.

        Example:
            ```python
            project = Projects(project_id="12345")
            updated_data = {"name": "New Project Name", "description": "Updated description."}
            response = project.update(updated_data)
            ```

        References:
            [requests.Response](https://docs.python-requests.org/en/latest/api/#requests.Response)
        """
        return super().update(self.id, data)

    def upload_image(self, file: str) -> Optional[Response]:
        """
        Uploads an image file to the hub associated with this client.

        Args:
            file (str): The file path or URL of the image to be uploaded.

        Returns:
            (Optional[Response]): Response object from the uploaded image request, or None if upload fails.

        Example:
            ```python
            projects = Projects(project_id="your_project_id")
            response = projects.upload_image("/path/to/your/image.jpg")
            if response:
                print("Image uploaded successfully")
            else:
                print("Image upload failed")
            ```

        References:
            - [Working with Response objects](https://requests.readthedocs.io/en/master/user/quickstart/#response-content)
        """
        return self.hub_client.upload_image(self.id, file)  # response


class ProjectList(PaginatedList):
    """
    A ProjectList class for managing a paginated list of project resources.

    This class extends the PaginatedList class to handle paginated fetching and management of project resources from the
    Ultralytics Hub API.

    Attributes:
        page_size (int | None): Number of items to request per page.
        public (bool | None): If True, retrieves only publicly accessible items.
        headers (dict | None): HTTP headers to include in API requests.

    Methods:
        get_page: Fetches a specific page of project resources.
        filter: Filters the fetched project resources based on specified criteria.

    Example:
        ```python
        project_list = ProjectList(page_size=10, public=True)
        first_page = project_list.get_page(1)
        for project in first_page:
            print(project["name"])
        ```

    References:
        - [Ultralytics Hub SDK Documentation](https://docs.ultralytics.com/)
    """

    def __init__(self, page_size: int = None, public: bool = None, headers: dict = None):
        """
        Initializes a ProjectList instance for paginated access to project resources.

        Args:
            page_size (int, optional): The number of items to request per page.
            public (bool, optional): Whether the items should be publicly accessible.
            headers (dict, optional): Headers to be included in API requests.

        Returns:
            (None): This constructor does not return a value.

        Example:
            ```python
            project_list = ProjectList(page_size=10, public=True)
            ```
        """
        base_endpoint = "projects"
        super().__init__(base_endpoint, "project", page_size, public, headers)
