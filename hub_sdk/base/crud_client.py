# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from typing import Optional

from requests import Response

from hub_sdk.base.api_client import APIClient
from hub_sdk.config import HUB_FUNCTIONS_ROOT
from hub_sdk.helpers.logger import logger


class CRUDClient(APIClient):
    """
    Represents a CRUD (Create, Read, Update, Delete) client for interacting with a specific resource.

    This class provides methods for performing standard CRUD operations on API resources, handling errors gracefully
    and providing logging for failed operations.

    Attributes:
        name (str): The name associated with the CRUD operations (e.g., "User").
        logger (logging.Logger): An instance of the logger for logging purposes.
    """

    def __init__(self, base_endpoint: str, name: str, headers: dict):
        """
        Initialize a CRUDClient instance.

        Args:
            base_endpoint (str): The base endpoint URL for the API.
            name (str): The name associated with the CRUD operations (e.g., "User").
            headers (dict): Headers to be included in API requests.
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
            (Optional[Response]): Response object from the create request, or None if creation fails.
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
            (Optional[Response]): Response object from the read request, or None if retrieval fails.
        """
        try:
            return self.get(f"/{id}")
        except Exception as e:
            self.logger.error(f"Failed to read {self.name} with ID: {id}, {e}")

    def update(self, id: str, data: dict) -> Optional[Response]:
        """
        Update an existing entity using the API.

        Args:
            id (str): The unique identifier of the entity to update.
            data (dict): The updated data to be sent in the update request.

        Returns:
            (Optional[Response]): Response object from the update request, or None if update fails.
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
            hard (bool, optional): If True, perform a hard delete. If False, perform a soft delete.

        Returns:
            (Optional[Response]): Response object from the delete request, or None if deletion fails.
        """
        try:
            return super().delete(f"/{id}", {"hard": hard})
        except Exception as e:
            self.logger.error(f"Failed to delete {self.name} with ID: {id}, {e}")

    def list(self, page: int = 0, limit: int = 10) -> Optional[Response]:
        """
        List entities using the API with pagination support.

        Args:
            page (int, optional): The page number to retrieve.
            limit (int, optional): The maximum number of entities per page.

        Returns:
            (Optional[Response]): Response object from the list request, or None if listing fails.
        """
        try:
            params = {"page": page, "limit": limit}
            return self.get("", params=params)
        except Exception as e:
            self.logger.error(f"Failed to list {self.name}: {e}")
