# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from typing import Any, Dict, Optional

from requests import Response

from hub_sdk.base.crud_client import CRUDClient
from hub_sdk.base.paginated_list import PaginatedList
from hub_sdk.base.server_clients import ProjectUpload


class Projects(CRUDClient):
    """
    A class representing a client for interacting with Projects through CRUD operations.

    This class extends the CRUDClient class and provides specific methods for working with Projects.

    Attributes:
        hub_client (ProjectUpload): An instance of ProjectUpload used for interacting with model uploads.
        id (str | None): The unique identifier of the project, if available.
        data (Dict): A dictionary to store project data.

    Note:
        The 'id' attribute is set during initialization and can be used to uniquely identify a project.
        The 'data' attribute is used to store project data fetched from the API.
    """

    def __init__(self, project_id: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        """
        Initialize a Projects object for interacting with project data via CRUD operations.

        Args:
            project_id (str, optional): Project ID for retrieving data.
            headers (Dict[str, Any], optional): A dictionary of HTTP headers to be included in API requests.
        """
        super().__init__("projects", "project", headers)
        self.hub_client = ProjectUpload(headers)
        self.id = project_id
        self.data = {}
        if project_id:
            self.get_data()

    def get_data(self) -> None:
        """
        Retrieve data for the current project instance.

        If a valid project ID has been set, it sends a request to fetch the project data and stores it in the instance.
        If no project ID has been set, it logs an error message.
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

    def create_project(self, project_data: Dict) -> None:
        """
        Create a new project with the provided data and set the project ID for the current instance.

        Args:
            project_data (Dict): A dictionary containing the data for creating the project.
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

    def update(self, data: Dict) -> Optional[Response]:
        """
        Update the project resource represented by this instance.

        Args:
            data (Dict): The updated data for the project resource.

        Returns:
            (Optional[Response]): Response object from the update request, or None if update fails.
        """
        return super().update(self.id, data)

    def upload_image(self, file: str) -> Optional[Response]:
        """
        Upload an image file to the hub associated with this client.

        Args:
            file (str): The file path or URL of the image to be uploaded.

        Returns:
            (Optional[Response]): Response object from the uploaded image request, or None if upload fails.
        """
        return self.hub_client.upload_image(self.id, file)  # response


class ProjectList(PaginatedList):
    """Provides a paginated list interface for querying project resources from the server."""

    def __init__(self, page_size: Optional[int] = None, public: Optional[bool] = None, headers: Optional[Dict] = None):
        """
        Initialize a ProjectList instance.

        Args:
            page_size (int, optional): The number of items to request per page.
            public (bool, optional): Whether the items should be publicly accessible.
            headers (Dict, optional): Headers to be included in API requests.
        """
        base_endpoint = "projects"
        super().__init__(base_endpoint, "project", page_size, public, headers)
