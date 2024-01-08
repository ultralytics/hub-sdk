from hub_sdk.base.crud_client import CRUDClient


class Users(CRUDClient):
    def __init__(self, user_id=None, headers=None):
        """
        Initialize a Userss object for interacting with user data via CRUD operations.

        Args:
            arg (str or dict): Either an ID (string) or data (dictionary) for the user.
            headers (dict, optional): A dictionary of HTTP headers to be included in API requests.
                                      Defaults to None.
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

        Args:
            None

        Returns:
            None
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
            None
        """
        resp = super().create(user_data).json()
        self.id = resp.get("data", {}).get("id")
        self.get_data()

    def delete(self, hard: bool = False):
        """
        Delete the user.

        Args:
            hard (bool, optional): If True, perform a hard delete. If False, perform a soft delete.
                                   Defaults to True.

        Returns:
            dict: A dictionary containing the response data from the server if the delete
                  operation was successful.
                  None if the operation fails.
        """
        return super().delete(self.id, hard)

    def update(self, data: dict) -> dict:
        """
        Update the user's data.

        Args:
            data (dict): The updated data for the users.

        Returns:
            dict: A dictionary containing the response data from the server if the update
                  operation was successful.
                  None if the operation fails.
        """
        return super().update(self.id, data)

    def cleanup(self, id: str):
        """
        Attempt to delete a users's data from the server.

        This method sends a DELETE request to the server in order to clean up a user's data.
        If the deletion is successful, the user's data will be removed from the server.

        Args:
            id (int or str): The unique identifier of the user to be cleaned up.

        Returns:
            dict: A dictionary containing the response data from the server if the cleanup
                  operation was successful.
                  None if the operation fails.

        Raises:
            Exception: If there is an issue with the API request or response during cleanup.
        """
        try:
            return self.delete(f"/{id}")
        except Exception as e:
            self.logger.error("Failed to cleanup: %s", e)
