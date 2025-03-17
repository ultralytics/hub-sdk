# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from typing import Any, Dict, Optional

from requests import Response

from hub_sdk.base.crud_client import CRUDClient
from hub_sdk.base.paginated_list import PaginatedList


class Teams(CRUDClient):
    """
    A class representing a client for interacting with Teams through CRUD operations.

    This class extends the CRUDClient class and provides specific methods for working with Teams.

    Attributes:
        id (str | None): The unique identifier of the team, if available.
        data (Dict): A dictionary to store team data.

    Note:
        The 'id' attribute is set during initialization and can be used to uniquely identify a team.
        The 'data' attribute is used to store team data fetched from the API.
    """

    def __init__(self, team_id: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        """
        Initialize a Teams instance.

        Args:
            team_id (str, optional): The unique identifier of the team.
            headers (Dict[str, Any], optional): A dictionary of HTTP headers to be included in API requests.
        """
        super().__init__("teams", "team", headers)
        self.id = team_id
        self.data = {}
        if team_id:
            self.get_data()

    def get_data(self) -> None:
        """
        Retrieve data for the current team instance.

        If a valid team ID has been set, it sends a request to fetch the team data and stores it in the instance. If no
        team ID has been set, it logs an error message.
        """
        if not self.id:
            self.logger.error("No team id has been set. Update the team id or create a team.")
            return

        try:
            response = super().read(self.id)

            if response is None:
                self.logger.error(f"Received no response from the server for team ID: {self.id}")
                return

            # Check if the response has a .json() method (it should if it's a response object)
            if not hasattr(response, "json"):
                self.logger.error(f"Invalid response object received for team ID: {self.id}")
                return

            resp_data = response.json()
            if resp_data is None:
                self.logger.error(f"No data received in the response for team ID: {self.id}")
                return

            data = resp_data.get("data", {})
            self.data = self._reconstruct_data(data)
            self.logger.debug(f"Team data retrieved for ID: {self.id}")

        except Exception as e:
            self.logger.error(f"An error occurred while retrieving data for team ID: {self.id}, {str(e)}")

    def create_team(self, team_data: Dict[str, Any]) -> None:
        """
        Create a new team with the provided data and set the team ID for the current instance.

        Args:
            team_data (Dict[str, Any]): A dictionary containing the data for creating the team.
        """
        resp = super().create(team_data).json()
        self.id = resp.get("data", {}).get("id")
        self.get_data()

    def delete(self, hard: bool = False) -> Optional[Response]:
        """
        Delete the team resource represented by this instance.

        Args:
            hard (bool, optional): If True, perform a hard (permanent) delete.

        Note:
            The 'hard' parameter determines whether to perform a soft delete (default) or a hard delete.
            In a soft delete, the team might be marked as deleted but retained in the system.
            In a hard delete, the team is permanently removed from the system.

        Returns:
            (Optional[Response]): The response from the delete request, or None if it fails.
        """
        return super().delete(self.id, hard)

    def update(self, data: Dict[str, Any]) -> Optional[Response]:
        """
        Update the team resource represented by this instance.

        Args:
            data (Dict[str, Any]): The updated data for the team resource.

        Returns:
            (Optional[Response]): The response from the update request, or None if it fails.
        """
        return super().update(self.id, data)


class TeamList(PaginatedList):
    """Provides a paginated list interface for managing and retrieving teams via API requests."""

    def __init__(
        self, page_size: Optional[int] = None, public: Optional[bool] = None, headers: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a TeamList instance.

        Args:
            page_size (int, optional): The number of items to request per page.
            public (bool, optional): Whether the items should be publicly accessible.
            headers (Dict[str, Any], optional): Headers to be included in API requests.
        """
        base_endpoint = "datasets"
        if public:
            base_endpoint = f"public/{base_endpoint}"
        super().__init__(base_endpoint, "team", page_size, headers)
