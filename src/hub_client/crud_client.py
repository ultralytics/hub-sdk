import logging

from .error_handler import ErrorHandler
from .api_client import APIClient, APIClientError
from .config import HUB_API_ROOT


class CRUDClient:
    def __init__(self, base_endpoint, name):
        self.api_client = APIClient(f"{HUB_API_ROOT}/{base_endpoint}")
        self.name = name
        self.logger = logging.getLogger(__name__)

    def _handle_request(self, request_func, *args, **kwargs):
        try:
            response = request_func(*args, **kwargs)
            response.raise_for_status()
            return response.json()
        except APIClientError as e:
            if e.status_code == 401:
                self.logger.error("Unauthorized: Please check your credentials.")
            else:
                self.logger.error(ErrorHandler(e.status_code))
            return None

    def create(self, data):
        try:
            return self._handle_request(self.api_client.post, "", data=data)
        except Exception as e:
            self.logger.error(f"Failed to create {self.name}: %s", e)

    def read(self, id):
        try:
            return self._handle_request(self.api_client.get, f"/{id}")
        except Exception as e:
            self.logger.error(f"Failed to read {self.name}: %s", e)

    def update(self, id, data):
        try:
            return self._handle_request(self.api_client.patch, f"/{id}", data=data)
        except Exception as e:
            self.logger.error(f"Failed to update {self.name}: %s", e)

    def delete(self, id, hard=False):
        try:
            if hard:
                return self._handle_request(self.api_client.delete, f"/{id}")
            else:
                soft_delete = {"dates": {"deleted": "SERVER_TIMESTAMP"}}
                return self.update(id, soft_delete)
        except Exception as e:
            self.logger.error(f"Failed to delete {self.name}: %s", e)

    def list(self, page=0, limit=10):
        try:
            params = {"page": page, "limit": limit}
            return self._handle_request(self.api_client.get, "", params=params)
        except Exception as e:
            self.logger.error(f"Failed to list {self.name}: %s", e)
