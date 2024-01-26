# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

from typing import Any, Optional, Dict
from requests import Response
from hub_sdk.base.crud_client import CRUDClient


class Users(CRUDClient):
    """
    A class representing a client for interacting with Users through CRUD operations. This class extends the CRUDClient
    class and provides specific methods for working with Users.

    Attributes:
        id (str, None): The unique identifier of the user, if available.
        data (dict): A dictionary to store user data.

    Note:
        The 'id' attribute is set during initialization and can be used to uniquely identify a user.
        The 'data' attribute is used to store user data fetched from the API.
    """

    def __init__(self, user_id: Optional[str] = None, headers: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize a Users object for interacting with user data via CRUD operations.

        Args:
            user_id (str, optional): The unique identifier of the user.
            headers (dict, optional): A dictionary of HTTP headers to be included in API requests.
        """
        super().__init__("users", "user", headers)
        self.id = user_id
        self.data = {}
        if user_id:
            self.get_data()

    def get_data(self) -> None:
        """
        Retrieves data for the current user instance.

        If a valid user ID has been set, it sends a request to fetch the user data and stores it in the instance.
        If no user ID has been set, it logs an error message.

        Returns:
            (None): The method does not return a value.
        """
        if self.id:
            resp = super().read(self.id).json()
            self.data = resp.get("data", {})
            self.logger.debug("user id is %s", self.id)
        else:
            self.logger.error("No user id has been set. Update the user id or create a user.")

    def create_user(self, user_data: dict) -> None:
        """
        Creates a new user with the provided data and sets the user ID for the current instance.

        Args:
            user_data (dict): A dictionary containing the data for creating the user.

        Returns:
            (None): The method does not return a value.
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

    def update(self, data: dict) -> Optional[Response]:
        """
        Update the user resource represented by this instance.

        Args:
            data (dict): The updated data for the user resource.

        Returns:
            (Optional[Response]): Response object from the update request, or None if update fails
        """
        return super().update(self.id, data)
