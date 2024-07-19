# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

from typing import Any, Dict, Optional

from requests import Response

from hub_sdk.base.crud_client import CRUDClient


class Users(CRUDClient):
    """
    A Users class for performing CRUD operations on user data via an API.

    This class extends the CRUDClient class and provides specific methods for creating, reading, updating, and deleting
    user resources.

    Attributes:
        id (str | None): The unique identifier of the user. Default is None.
        data (dict): A dictionary to store user data. Default is an empty dictionary.

    Methods:
        get_data: Retrieves data for the current user instance.
        create_user: Creates a new user with the provided data and sets the user ID for the current instance.
        delete: Deletes the user resource represented by this instance, optionally performing a hard delete.
        update: Updates the user resource with the provided data.

    Example:
        ```python
        user_client = Users(user_id='abc123')
        user_client.get_data()
        print(user_client.data)

        new_user_data = {'name': 'John Doe', 'email': 'john.doe@example.com'}
        user_client.create_user(new_user_data)

        update_data = {'name': 'John Smith'}
        user_client.update(update_data)

        user_client.delete(hard=True)
        ```

    References:
        [Requests Library](https://docs.python-requests.org/): Used for making HTTP requests.
    """

    def __init__(self, user_id: Optional[str] = None, headers: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize a Users object for interacting with user data via CRUD operations.

        Args:
            user_id (str | None): The unique identifier of the user.
            headers (dict[str, Any] | None): A dictionary of HTTP headers to be included in API requests.

        Returns:
            None

        Notes:
            The 'id' attribute is set during initialization and can be used to uniquely identify a user.
            The 'data' attribute is used to store user data fetched from the API.
        """
        super().__init__("users", "user", headers)
        self.id = user_id
        self.data = {}
        if user_id:
            self.get_data()

    def get_data(self) -> None:
        """
        Retrieves and stores data for the current user instance.

        If the user ID is set, the function sends a request to fetch the user data and stores it in the instance.
        If no user ID is set, it logs an error message.

        Args:
            None

        Returns:
            (None): The method does not return a value.

        Notes:
            The function relies on the user ID being set at initialization to fetch and store user data.

        References:
            [Requests Library](https://docs.python-requests.org/en/master/)
            [CRUD Operations](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)
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

    def create_user(self, user_data: dict) -> None:
        """
        Creates a new user with the provided data and sets the user ID for the current instance.

        Args:
            user_data (dict): A dictionary containing the data for creating the user.

        Returns:
            (None): The method does not return a value.

        Example:
            ```python
            users_instance = Users()
            user_data = {"name": "John Doe", "email": "john.doe@example.com"}
            users_instance.create_user(user_data)
            ```
        """
        resp = super().create(user_data).json()
        self.id = resp.get("data", {}).get("id")
        self.get_data()

    def delete(self, hard: bool = False) -> Optional[Response]:
        """
        Deletes the user resource represented by this instance.

        Args:
            hard (bool, optional): If True, perform a hard delete. A soft delete (default) marks the user as
                deleted but retains data; a hard delete permanently removes the user.

        Returns:
            (Optional[Response]): Response object from the delete request, or None if delete fails.

        Example:
            ```python
            user = Users(user_id="1234")
            response = user.delete(hard=True)
            ```

        Notes:
            - A hard delete removes the user data permanently, while a soft delete only flags the data as deleted.

        References:
            - [Python Requests Library](https://docs.python-requests.org/en/master/)
            - [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
        """
        return super().delete(self.id, hard)

    def update(self, data: dict) -> Optional[Response]:
        """
        Update the user resource represented by this instance.

        Args:
            data (dict): The updated data for the user resource.

        Returns:
            (Optional[Response]): Response object from the update request, or None if update fails.

        Example:
            ```python
            user = Users(user_id="12345")
            updated_data = {"name": "John Doe", "email": "john@example.com"}
            response = user.update(updated_data)
            if response:
                print("User updated successfully.", response.json())
            else:
                print("Failed to update user.")
            ```

        References:
            - [Python Requests Library](https://docs.python-requests.org/en/master/)
        """
        return super().update(self.id, data)
