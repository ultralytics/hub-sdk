# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from typing import Any, Dict, Optional

from requests import Response

from hub_sdk.base.crud_client import CRUDClient


class Users(CRUDClient):
    """
    A class representing a client for interacting with Users through CRUD operations.

    This class extends the CRUDClient class and provides specific methods for working with Users.

    Attributes:
        id (str | None): The unique identifier of the user, if available.
        data (Dict): A dictionary to store user data.

    Methods:
        get_data: Retrieves data for the current user instance.
        create_user: Creates a new user with the provided data.
        delete: Deletes the user resource represented by this instance.
        update: Updates the user resource represented by this instance.

    Note:
        The 'id' attribute is set during initialization and can be used to uniquely identify a user.
        The 'data' attribute is used to store user data fetched from the API.
    """

    def __init__(self, user_id: Optional[str] = None, headers: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize a Users object for interacting with user data via CRUD operations.

        Args:
            user_id (str, optional): The unique identifier of the user.
            headers (Dict[str, Any], optional): A dictionary of HTTP headers to be included in API requests.
        """
        super().__init__("users", "user", headers)
        self.id = user_id
        self.data = {}
        if user_id:
            self.get_data()

    def get_data(self) -> None:
        """
        Retrieve data for the current user instance.

        If a valid user ID has been set, it sends a request to fetch the user data and stores it in the instance. If no
        user ID has been set, it logs an error message.
        """
        if not self.id:
            self.logger.error("No user id has been set. Update the user id or create a user.")
            return

        try:
            response = super().read(self.id)

            if response is None:
                self.logger.error(f"Received no response from the server for user ID: {self.id}")
                return

            # Check if the response has a .json() method (it should if it's a response object)
            if not hasattr(response, "json"):
                self.logger.error(f"Invalid response object received for user ID: {self.id}")
                return

            resp_data = response.json()
            if resp_data is None:
                self.logger.error(f"No data received in the response for user ID: {self.id}")
                return

            data = resp_data.get("data", {})
            self.data = self._reconstruct_data(data)
            self.logger.debug(f"User data retrieved for ID: {self.id}")

        except Exception as e:
            self.logger.error(f"An error occurred while retrieving data for user ID: {self.id}, {str(e)}")

    def create_user(self, user_data: Dict) -> None:
        """
        Create a new user with the provided data and set the user ID for the current instance.

        Args:
            user_data (Dict): A dictionary containing the data for creating the user.
        """
        resp = super().create(user_data).json()
        self.id = resp.get("data", {}).get("id")
        self.get_data()

    def delete(self, hard: bool = False) -> Optional[Response]:
        """
        Delete the user resource represented by this instance.

        Args:
            hard (bool, optional): If True, perform a hard delete.

        Note:
            The 'hard' parameter determines whether to perform a soft delete (default) or a hard delete.
            In a soft delete, the model might be marked as deleted but retained in the system.
            In a hard delete, the model is permanently removed from the system.

        Returns:
            (Optional[Response]): Response object from the delete request, or None if delete fails
        """
        return super().delete(self.id, hard)

    def update(self, data: Dict) -> Optional[Response]:
        """
        Update the user resource represented by this instance.

        Args:
            data (Dict): The updated data for the user resource.

        Returns:
            (Optional[Response]): Response object from the update request, or None if update fails
        """
        return super().update(self.id, data)
