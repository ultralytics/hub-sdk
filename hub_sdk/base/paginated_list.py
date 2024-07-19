# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

import math
from typing import Optional

from requests import Response

from hub_sdk.base.api_client import APIClient
from hub_sdk.config import HUB_FUNCTIONS_ROOT


class PaginatedList(APIClient):
    """Handles paginated API responses by managing page state and fetching subsequent pages as needed."""

    def __init__(self, base_endpoint, name, page_size=None, public=None, headers=None):
        """
        Initialize a PaginatedList instance.

        Args:
            base_endpoint (str): The base API endpoint for the paginated resource.
            name (str): A descriptive name for the paginated resource.
            page_size (int, optional): The number of items per page.
            headers (dict, optional): Additional headers to include in API requests.
        """
        super().__init__(f"{HUB_FUNCTIONS_ROOT}/v1/{base_endpoint}", headers)
        self.name = name
        self.page_size = page_size
        self.public = public
        self.pages = [None]
        self.current_page = 0
        self.total_pages = 1
        self._get()

    def _get(self, query=None):
        """
        Retrieve data for the current page.

        Args:
            query (dict, optional): Additional query parameters for the API request.
        """
        try:
            last_record = self.pages[self.current_page]
            resp = self.list(
                self.page_size,
                last_record,
                query=query,
            )
            self.__update_data(resp)
        except Exception as e:
            self.results = []
            self.logger.error(f"Failed to get data: {e}")

    def previous(self) -> None:
        """Move to the previous page of results if available."""
        try:
            if self.current_page > 0:
                self.current_page -= 1
                self._get()
        except Exception as e:
            self.logger.error(f"Failed to get previous page: {e}")

    def next(self) -> None:
        """Move to the next page of results if available."""
        try:
            if self.current_page < self.total_pages - 1:
                self.current_page += 1
                self._get()
        except Exception as e:
            self.logger.error(f"Failed to get next page: {e}")

    def __update_data(self, resp: Response) -> None:
        """
        Update the internal data with the response from the API.

        Args:
            resp (Response): API response data.
        """
        if resp:
            resp_data = resp.json().get("data", {})
            self.results = resp_data.get("results", {})
            self.total_pages = math.ceil(resp_data.get("total") / self.page_size) if self.page_size > 0 else 0
            last_record_id = resp_data.get("lastRecordId")
            if last_record_id is None:
                self.pages[self.current_page + 1 :] = [None] * (len(self.pages) - self.current_page - 1)
            elif len(self.pages) <= self.current_page + 1:
                self.pages.append(last_record_id)
            else:
                self.pages[self.current_page + 1] = last_record_id
        else:
            self.results = {}
            self.total_pages = 0
            self.pages[self.current_page + 1 :] = [None] * (len(self.pages) - self.current_page - 1)

    def list(self, page_size: int = 10, last_record=None, query=None) -> Optional[Response]:
        """
        Retrieve a list of items from the API.

        Args:
            page_size (int, optional): The number of items per page.
            last_record (str, optional): ID of the last record from the previous page.
            query (dict, optional): Additional query parameters for the API request.

        Returns:
            (Optional[Response]): Response object from the list request, or None if it fails.
        """
        try:
            params = {"limit": page_size}
            if last_record:
                params["last_doc_id"] = last_record
            if query:
                params["query"] = query
            if self.public is not None:
                params["public"] = self.public
            return self.get("", params=params)
        except Exception as e:
            self.logger.error(f"Failed to list {self.name}: {e}")
