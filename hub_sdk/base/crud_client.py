from hub_sdk.base.api_client import APIClient
from hub_sdk.config import HUB_FUNCTIONS_ROOT
from hub_sdk.helpers.logger import logger


class CRUDClient(APIClient):
    def __init__(self, base_endpoint, name, headers):
        """
        Initialize a CRUDClient instance.

        Args:
            base_endpoint (str): The base endpoint URL for the API.
            name (str): The name associated with the CRUD operations (e.g., "User").
            headers (dict): Headers to be included in API requests.

        Returns:
            None
        """
        super().__init__(f"{HUB_FUNCTIONS_ROOT}/v1/{base_endpoint}", headers)
        self.name = name
        self.logger = logger

    def create(self, data: dict) -> dict:
        """
        Create a new entity using the API.

        Args:
            data (dict): The data to be sent as part of the creation request.

        Returns:
            dict or None: Created entity data if successful, None on failure.
        """
        try:
            return self.post("", json=data)
        except Exception as e:
            self.logger.error(f"Failed to create {self.name}: %s", e)

    def read(self, id: str) -> dict:
        """
        Retrieve details of a specific entity.

        Args:
            id (str): The unique identifier of the entity to retrieve.

        Returns:
            dict or None: Entity details if successful, None on failure.
        """
        try:
            return self.get(f"/{id}")
        except Exception as e:
            self.logger.error(f"Failed to read {self.name}: %s", e)

    def update(self, id: str, data: dict) -> dict:
        """
        Update an existing entity using the API.

        Args:
            id (str): The unique identifier of the entity to update.
            data (dict): The updated data to be sent in the update request.

        Returns:
            dict or None: Updated entity data if successful, None on failure.
        """
        try:
            return self.patch(f"/{id}", json=data)
        except Exception as e:
            self.logger.error(f"Failed to update {self.name}: %s", e)

    def delete(self, id: str, hard: bool = False) -> dict:
        """
        Delete an entity using the API.

        Args:
            id (str): The unique identifier of the entity to delete.
            hard (bool, optional): If True, perform a hard delete. If False, perform a soft delete.
                Default is False.

        Returns:
            dict or None: Deleted entity data if successful, None on failure.
        """
        try:
            return super().delete(f"/{id}", hard)
        except Exception as e:
            self.logger.error(f"Failed to delete {self.name}: %s", e)

    def list(self, page: int = 0, limit: int = 10) -> dict:
        """
        List entities using the API.

        Args:
            page (int, optional): The page number to retrieve. Default is 0.
            limit (int, optional): The maximum number of entities per page. Default is 10.

        Returns:
            dict or None: List of entities if successful, None on failure.
        """
        try:
            params = {"page": page, "limit": limit}
            return self.get("", params=params)
        except Exception as e:
            self.logger.error(f"Failed to list {self.name}: %s", e)
