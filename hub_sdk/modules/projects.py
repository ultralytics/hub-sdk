# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

from typing import Any, Dict, Optional
from requests import Response
from hub_sdk.base.crud_client import CRUDClient
from hub_sdk.base.paginated_list import PaginatedList
from hub_sdk.base.server_clients import ProjectUpload


class Projects(CRUDClient):
    """
    A class representing a client for interacting with Projects through CRUD operations. This class extends the
    CRUDClient class and provides specific methods for working with Projects.

    Attributes:
        hub_client (ProjectUpload): An instance of ProjectUpload used for interacting with model uploads.
        id (str, None): The unique identifier of the project, if available.
        data (dict): A dictionary to store project data.

    Note:
        The 'id' attribute is set during initialization and can be used to uniquely identify a project.
        The 'data' attribute is used to store project data fetched from the API.
    """

    def __init__(self, project_id: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        """
        Initialize a Projects object for interacting with project data via CRUD operations.

        Args:
            project_id (str, optional): Project ID for retrieving data.
            headers (dict, optional): A dictionary of HTTP headers to be included in API requests.
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

        If a valid project ID has been set, it sends a request to fetch the project data and stores it in the instance.
        If no project ID has been set, it logs an error message.

        Returns:
            (None): The method does not return a value.
        """
        if self.id:
            resp = super().read(self.id).json()
            self.data = resp.get("data", {})
            self.logger.debug("Project id is %s", self.id)
        else:
            self.logger.error("No project id has been set. Update the project id or create a project.")

    def create_project(self, project_data: dict) -> None:
        """
        Creates a new project with the provided data and sets the project ID for the current instance.

        Args:
            project_data (dict): A dictionary containing the data for creating the project.

        Returns:
            (None): The method does not return a value.
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
            In a soft delete, the project might be marked as deleted but retained in the system.
            In a hard delete, the project is permanently removed from the system.

        Returns:
            (Optional[Response]): Response object from the delete request, or None if delete fails.
        """
        return super().delete(self.id, hard)

    def update(self, data: dict) -> Optional[Response]:
        """
        Update the project resource represented by this instance.

        Args:
            data (dict): The updated data for the project resource.

        Returns:
            (Optional[Response]): Response object from the update request, or None if update fails.
        """
        return super().update(self.id, data)

    def upload_image(self, file: str) -> Optional[Response]:
        """
        Uploads an image file to the hub associated with this client.

        Args:
            file (str): The file path or URL of the image to be uploaded.

        Returns:
            (Optional[Response]): Response object from the uploaded image request, or None if upload fails.
        """
        return self.hub_client.upload_image(self.id, file)  # response


class ProjectList(PaginatedList):
    def __init__(self, page_size: int = None, public: bool = None, headers: dict = None):
        """
        Initialize a ProjectList instance.

        Args:
            page_size (int, optional): The number of items to request per page.
            public (bool, optional): Whether the items should be publicly accessible.
            headers (dict, optional): Headers to be included in API requests.
        """
        base_endpoint = "projects"
        if public:
            base_endpoint = f"public/{base_endpoint}"
        super().__init__(base_endpoint, "project", page_size, headers)
