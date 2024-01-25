# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

from typing import Any, Optional, Dict
from requests import Response
from hub_sdk.base.crud_client import CRUDClient
from hub_sdk.base.paginated_list import PaginatedList


class Teams(CRUDClient):
    """
    A class representing CRUD operations for managing teams.

    This class extends the CRUDClient class to provide specific functionality for managing teams. It inherits common
    CRUD (Create, Read, Update, Delete) operations from the parent class.
    """

    def __init__(self, team_id: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        """
        Initialize a Teams instance.

        Args:
            team_id (str, optional): The unique identifier of the team. Defaults to None.
            headers (dict, optional): A dictionary of HTTP headers to be included in API requests.
                                      Defaults to None.
        """
        super().__init__("teams", "team", headers)
        self.id = team_id
        self.data = {}
        if team_id:
            self.get_data()

    def get_data(self) -> None:
        """
        Retrieves data for the current team instance.

        If a valid team ID has been set, it sends a request to fetch the team data and stores it in the instance.
        If no team ID has been set, it logs an error message.

        Returns:
            (None)
        """
        if self.id:
            resp = super().read(self.id).json()
            self.data = resp.get("data", {})
            self.logger.debug("Team id is %s", self.id)
        else:
            self.logger.error("No team id has been set. Update the team id or create a team.")

    def create_team(self, team_data) -> None:
        """
        Creates a new team with the provided data and sets the team ID for the current instance.

        Args:
            team_data (dict): A dictionary containing the data for creating the team.

        Returns:
            (None)
        """
        resp = super().create(team_data).json()
        self.id = resp.get("data", {}).get("id")
        self.get_data()

    def delete(self, hard=False) -> Optional[Response]:
        """
        Delete the team.

        Args:
            hard (bool, optional): If True, perform a hard delete. Defaults to True.

        Returns:
            (Optional[Response]): The response from the delete request, or None if it fails.
        """
        return super().delete(self.id, hard)

    def update(self, data) -> Optional[Response]:
        """
        Update the team's data.

        Args:
            data (dict): The updated data for the team.

        Returns:
            (Optional[Response]): The response from the update request, or Noe if it fails.
        """
        return super().update(self.id, data)

    def cleanup(self, id) -> Optional[Response]:
        """
        Clean up a team by deleting it from the system.

        This method sends a delete request to the API to remove the team with
        the specified ID.

        Args:
            id (str): The unique identifier of the team to be cleaned up.

        Returns:
            (Optional[Response]): Response object from the cleanup request, or None if cleanup fails
        """
        try:
            return self.delete(f"/{id}")
        except Exception as e:
            self.logger.error("Failed to cleanup: %s", e)


class TeamList(PaginatedList):
    def __init__(self, page_size=None, public=None, headers=None):
        """
        Initialize a TeamList instance.

        Args:
            page_size (int, optional): The number of items to request per page. Defaults to None.
            public (bool, optional): Whether the items should be publicly accessible. Defaults to None.
            headers (dict, optional): Headers to be included in API requests. Defaults to None.
        """
        base_endpoint = "datasets"
        if public:
            base_endpoint = f"public/{base_endpoint}"
        super().__init__(base_endpoint, "team", page_size, headers)
