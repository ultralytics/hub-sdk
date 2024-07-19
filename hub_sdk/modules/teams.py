# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

from typing import Any, Dict, Optional

from requests import Response

from hub_sdk.base.crud_client import CRUDClient
from hub_sdk.base.paginated_list import PaginatedList


class Teams(CRUDClient):
    """
    A class representing a client for interacting with Teams through CRUD operations.

    This class extends the CRUDClient class and provides specific methods for working with Teams. It allows users to
    create, read, update, and delete team data.

    Attributes:
        id (str | None): The unique identifier of the team, if available.
        data (dict): A dictionary to store team data.

    Methods:
        get_data: Retrieves data for the current team instance.
        create_team: Creates a new team with the provided data.
        delete: Deletes the team resource represented by this instance.
        update: Updates the team resource represented by this instance.

    Example:
        ```python
        team_client = Teams(team_id='1234abcd', headers={'Authorization': 'Bearer your_token'})
        team_client.get_data()
        print(team_client.data)

        new_team_data = {"name": "New Team"}
        team_client.create_team(new_team_data)
        ```

    References:
        - [requests.Response](https://docs.python-requests.org/en/master/api/#requests.Response)
        - [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
    """

    def __init__(self, team_id: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        """
        Initializes a Teams instance for interacting with team-related CRUD operations.

        Args:
            team_id (str | None, optional): The unique identifier of the team.
            headers (dict | None, optional): A dictionary of HTTP headers to be included in API requests,
                allowing for customization and authentication.

        Returns:
            None

        Notes:
            Inherits from CRUDClient to provide specific methods for handling team data via CRUD operations.

        Example:
            ```python
            headers = {"Authorization": "Bearer YOUR_ACCESS_TOKEN"}
            team = Teams(team_id="12345", headers=headers)
            ```

        References:
            - [RESTful APIs](https://restfulapi.net/)
        """
        super().__init__("teams", "team", headers)
        self.id = team_id
        self.data = {}
        if team_id:
            self.get_data()

    def get_data(self) -> None:
        """
        Retrieves data for the current team instance.

        If a valid team ID is set, it fetches the team data and stores it in the instance. Logs an error if no team ID is set.

        Returns:
            (None): The method does not return a value.

        Notes:
            - Requires a valid team ID to fetch data. Logs an error message if team ID is not set.
            - Fetches team data via an API call and stores it in the instance's `data` attribute.
            - Handles potential errors by logging appropriate error messages.
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

    def create_team(self, team_data) -> None:
        """
        Creates a new team with the provided data and sets the team ID for the current instance.

        Args:
            team_data (dict): A dictionary containing the data required to create the team.

        Returns:
            (None): The method does not return a value.

        Example:
            ```python
            team_data = {
                "name": "Engineering",
                "description": "Team responsible for product development and maintenance."
            }
            teams_instance = Teams()
            teams_instance.create_team(team_data)
            ```

        Notes:
            Ensure that the `team_data` dictionary contains all mandatory fields required by the API for creating a team.
        """
        resp = super().create(team_data).json()
        self.id = resp.get("data", {}).get("id")
        self.get_data()

    def delete(self, hard=False) -> Optional[Response]:
        """
        Delete the team resource represented by this instance.

        Args:
            hard (bool, optional): If True, perform a hard (permanent) delete. Default is False for a soft delete.

        Returns:
            (Optional[Response]): The response from the delete request, or None if it fails.

        Notes:
            The 'hard' parameter determines whether to perform a soft delete (default) or a hard delete.
            In a soft delete, the team might be marked as deleted but retained in the system. In a hard delete,
            the team is permanently removed from the system.

        References:
            [Requests Library Documentation](https://docs.python-requests.org/en/master/)
        """
        return super().delete(self.id, hard)

    def update(self, data) -> Optional[Response]:
        """
        Update the team resource represented by this instance.

        Args:
            data (dict): The updated data for the team resource.

        Returns:
            (Optional[Response]): The response from the update request, or None if it fails.

        Example:
            ```python
            team = Teams(team_id="1234")
            update_data = {"name": "New Team Name", "description": "Updated description"}
            response = team.update(update_data)
            ```

        References:
            [requests.Response](https://docs.python-requests.org/en/master/api/#requests.Response)
        """
        return super().update(self.id, data)


class TeamList(PaginatedList):
    """
    A class for managing and paginating through lists of teams accessible via the Ultralytics HUB-SDK.

    Attributes:
        page_size (int | None): Number of items to request per page.
        public (bool | None): Whether the items should be publicly accessible.
        headers (dict | None): Headers to include in API requests.

    Methods:
        __init__: Initializes a TeamList instance.

    Example:
        ```python
        team_list = TeamList(page_size=10, public=True, headers={'Authorization': 'Bearer YOUR_TOKEN'})
        teams = team_list.fetch_next_page()
        for team in teams:
            print(team['name'])
        ```

    References:
        [Requests - HTTP for Humans](https://docs.python-requests.org/en/master/)
    """

    def __init__(self, page_size=None, public=None, headers=None):
        """
        Initialize a TeamList instance.

        Args:
            page_size (int, optional): The number of items to request per page.
            public (bool, optional): Whether the items should be publicly accessible.
            headers (dict, optional): Headers to be included in API requests.

        Returns:
            (None): The method does not return a value.

        Notes:
            The `base_endpoint` is set to "datasets" by default. If `public` is True, it changes to "public/datasets".
        """
        base_endpoint = "datasets"
        if public:
            base_endpoint = f"public/{base_endpoint}"
        super().__init__(base_endpoint, "team", page_size, headers)
