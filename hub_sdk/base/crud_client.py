# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

from typing import Optional

from requests import Response

from hub_sdk.base.api_client import APIClient
from hub_sdk.config import HUB_FUNCTIONS_ROOT
from hub_sdk.helpers.logger import logger


class CRUDClient(APIClient):
    """
    Represents a CRUD (Create, Read, Update, Delete) client for interacting with specific resources via API calls.

    Attributes:
        name (str): The name associated with the CRUD operations (e.g., "User").
        logger (logging.Logger): An instance of the logger for logging purposes.

    Methods:
        create: Creates a new entity using the API.
        read: Retrieves details of a specific entity.
        update: Updates an existing entity using the API.
        delete: Deletes an entity using the API.
        list: Lists entities using the API.

    Example:
        ```python
        crud_client = CRUDClient(base_endpoint='users', name='User', headers={'Authorization': 'Bearer ...'})
        response = crud_client.create(data={'name': 'John Doe'})
        if response:
            print('Created User:', response.json())
        ```

    References:
        - [Requests library](https://docs.python-requests.org/en/master/): Python HTTP for Humans.
    """

    def __init__(self, base_endpoint, name, headers):
        """
        Initializes a CRUDClient instance for interacting with a specific resource.

        Args:
            base_endpoint (str): The base endpoint URL for the API.
            name (str): The name associated with the CRUD operations (e.g., "User").
            headers (dict): Headers to be included in API requests.

        Returns:
            None

        Example:
            ```python
            client = CRUDClient(base_endpoint="users", name="User", headers={"Authorization": "Bearer token"})
            ```

        References:
            - [requests Library](https://docs.python-requests.org/en/latest/user/quickstart/)
            - [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
        """
        super().__init__(f"{HUB_FUNCTIONS_ROOT}/v1/{base_endpoint}", headers)
        self.name = name
        self.logger = logger

    def create(self, data: dict) -> Optional[Response]:
        """
        Create a new entity using the API.

        Args:
            data (dict): The data to be sent as part of the creation request.

        Returns:
            (Optional[Response]): Response object from the create request, or None if upload fails.

        Example:
            ```python
            client = CRUDClient(base_endpoint="users", name="User", headers={"Authorization": "Bearer token"})
            data = {"name": "John Doe", "email": "johndoe@example.com"}
            response = client.create(data)
            if response:
                print("User created successfully")
            else:
                print("Failed to create user")
            ```

        References:
            [Requests Library Documentation](https://docs.python-requests.org/en/latest/)
        """
        try:
            return self.post("", json=data)
        except Exception as e:
            self.logger.error(f"Failed to create {self.name}: {e}")

    def read(self, id: str) -> Optional[Response]:
        """
        Retrieve details of a specific entity.

        Args:
            id (str): The unique identifier of the entity to retrieve.

        Returns:
            (Optional[Response]): Response object from the read request, or None if read fails.

        Example:
            ```python
            client = CRUDClient(base_endpoint='entities', name='Entity', headers={})
            response = client.read(id='123')
            if response:
                print(response.json())
            ```
        """
        try:
            return self.get(f"/{id}")
        except Exception as e:
            self.logger.error(f"Failed to read {self.name} with ID: {id}, {e}")

    def update(self, id: str, data: dict) -> Optional[Response]:
        """
        Updates an existing entity using the API.

        Args:
            id (str): The unique identifier of the entity to update.
            data (dict): The updated data to be sent in the update request.

        Returns:
            (Optional[Response]): Response object from the update request, or None if the update fails.

        Example:
            ```python
            client = CRUDClient(base_endpoint="users", name="User", headers={"Authorization": "Bearer token"})
            response = client.update(id="12345", data={"name": "New Name"})
            ```
        """
        try:
            return self.patch(f"/{id}", json=data)
        except Exception as e:
            self.logger.error(f"Failed to update {self.name} with ID: {id}, {e}")

    def delete(self, id: str, hard: bool = False) -> Optional[Response]:
        """
        Delete an entity using the API.

        Args:
            id (str): The unique identifier of the entity to delete.
            hard (bool, optional): If True, perform a hard delete. If False, perform a soft delete. Defaults to False.

        Returns:
            (Optional[Response]): Response object from the delete request, or None if delete fails.

        Example:
            ```python
            client = CRUDClient(base_endpoint="entity", name="Entity", headers={"Authorization": "Bearer token"})
            response = client.delete("1234", hard=True)
            ```
        """
        try:
            return super().delete(f"/{id}", {"hard": hard})
        except Exception as e:
            self.logger.error(f"Failed to delete {self.name} with ID: {id}, {e}")

    def list(self, page: int = 0, limit: int = 10) -> Optional[Response]:
        """
        List entities using the API.

        Args:
            page (int, optional): The page number to retrieve.
            limit (int, optional): The maximum number of entities per page.

        Returns:
            (Optional[Response]): Response object from the list request, or None if it fails.

        Example:
            ```python
            client = CRUDClient("entities", "Entity", headers={"Authorization": "Bearer token"})
            response = client.list(page=1, limit=20)
            entities = response.json() if response else []
            ```

        References:
            - [requests.Response](https://docs.python-requests.org/en/latest/api/#requests.Response)
        """
        try:
            params = {"page": page, "limit": limit}
            return self.get("", params=params)
        except Exception as e:
            self.logger.error(f"Failed to list {self.name}: {e}")
