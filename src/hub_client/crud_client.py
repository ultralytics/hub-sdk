from .error_handler import ErrorHandler
from .logger import Logger
from .api_client import APIClient, APIClientError
from .config import HUB_API_ROOT


class CRUDClient:
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
        self.api_client = APIClient(f"{HUB_API_ROOT}/{base_endpoint}", headers=headers)
        self.name = name
        self.logger = Logger(__name__).get_logger()

    def _handle_request(self, request_func, *args, **kwargs):
        """
        Handles an API request, logging errors and handling exceptions.

        Args:
            request_func (callable): The API request function to be executed.
            *args: Variable length argument list for the request function.
            **kwargs: Arbitrary keyword arguments for the request function.

        Returns:
            dict or None: Parsed JSON response if successful, None on failure.
        """
        try:
            response = request_func(*args, **kwargs)
            response.raise_for_status()
            return response.json()
        except APIClientError as e:
            if e.status_code == 401:
                self.logger.error("Unauthorized: Please check your credentials.")
            else:
                self.logger.error(ErrorHandler(e.status_code).handle())
            return None

    def create(self, data):
        """
        Create a new entity using the API.

        Args:
            data (dict): The data to be sent as part of the creation request.

        Returns:
            dict or None: Created entity data if successful, None on failure.
        """
        try:
            return self._handle_request(self.api_client.post, "", data=data)
        except Exception as e:
            self.logger.error(f"Failed to create {self.name}: %s", e)

    def read(self, id):
        """
        Retrieve details of a specific entity.

        Args:
            id (str): The unique identifier of the entity to retrieve.

        Returns:
            dict or None: Entity details if successful, None on failure.
        """
        try:
            return self._handle_request(self.api_client.get, f"/{id}")
        except Exception as e:
            self.logger.error(f"Failed to read {self.name}: %s", e)

    def update(self, id, data):
        """
        Update an existing entity using the API.

        Args:
            id (str): The unique identifier of the entity to update.
            data (dict): The updated data to be sent in the update request.

        Returns:
            dict or None: Updated entity data if successful, None on failure.
        """
        try:
            return self._handle_request(self.api_client.patch, f"/{id}", data=data)
        except Exception as e:
            self.logger.error(f"Failed to update {self.name}: %s", e)

    def delete(self, id, hard=False):
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
            return self._handle_request(self.api_client.delete, f"/{id}", hard)
        except Exception as e:
            self.logger.error(f"Failed to delete {self.name}: %s", e)

    def list(self, page=0, limit=10):
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
            return self._handle_request(self.api_client.get, "", params=params)
        except Exception as e:
            self.logger.error(f"Failed to list {self.name}: %s", e)
