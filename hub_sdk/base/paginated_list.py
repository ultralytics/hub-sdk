# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

import math
from typing import Optional

from requests import Response

from hub_sdk.base.api_client import APIClient
from hub_sdk.config import HUB_FUNCTIONS_ROOT


class PaginatedList(APIClient):
    """
    A PaginatedList class for managing paginated API resources.

    This class facilitates retrieving, navigating, and updating paginated data from an API endpoint in a structured manner.

    Attributes:
        name (str): A descriptive name for the paginated resource.
        page_size (int | None): The number of items per page, if specified.
        public (bool | None): Flag indicating whether the resource is public.
        pages (list): List tracking page states for pagination.
        current_page (int): Current active page index.
        total_pages (int): Total number of pages available.

    Methods:
        previous: Move to the previous page of results if available.
        next: Move to the next page of results if available.
        list: Retrieve a list of items from the API.
        _get: Retrieve data for the current page.
        __update_data: Update the internal data with the response from the API.

    Example:
        ```python
        paginated_list = PaginatedList(base_endpoint='items', name='Items', page_size=20)
        paginated_list.next()  # Move to the next page of items
        paginated_list.previous()  # Move back to the previous page
        ```

    References:
        [requests library](https://docs.python-requests.org/en/latest/) - For making HTTP requests.
    """

    def __init__(self, base_endpoint, name, page_size=None, public=None, headers=None):
        """
        Initializes a PaginatedList instance.

        Args:
            base_endpoint (str): The base API endpoint for the paginated resource.
            name (str): A descriptive name for the paginated resource.
            page_size (int | None): The number of items per page.
            public (bool | None): Indicates if the resource is public.
            headers (dict | None): Additional headers to include in API requests.

        Returns:
            None

        Notes:
            This constructor sets up the base attributes for managing a paginated resource via API.

        References:
            [requests](https://docs.python-requests.org/en/latest/)
            [HUB SDK](https://github.com/ultralytics/hub-sdk)
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
        Performs retrieval of data for the current page from the paginated API endpoint.

        Args:
            query (dict | None): Additional query parameters for the API request.

        Returns:
            (Response | None): The API response containing the paginated data or None if an exception occurred.

        Notes:
            This method handles updating the internal state of the PaginatedList instance with the data retrieved
            from the API. Exceptions are caught and result in an empty list stored in `self.results`.

        References:
            [requests.Response](https://docs.python-requests.org/en/master/api/#requests.Response)
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
        """
        Moves to the previous page of results if available.

        Returns:
            (None): This function does not return any value.

        Notes:
            Decrements the `current_page` attribute and fetches data using the `_get` method. Raises an exception
            if attempting to move to a previous page when `current_page` is 0.
        """
        try:
            if self.current_page > 0:
                self.current_page -= 1
                self._get()
        except Exception as e:
            self.logger.error(f"Failed to get previous page: {e}")

    def next(self) -> None:
        """
        Moves to the next page of results if available.

        Returns:
            None

        Notes:
            This function will increment the current page index and fetch data for the next page only if the
            current page is not the last one.

        Example:
            ```python
            paginated_list = PaginatedList('endpoint', 'resource_name', page_size=10)
            paginated_list.next()  # Move to the next page if it exists
            ```

        References:
            [Python Requests Documentation](https://docs.python-requests.org/)
            [Ultralytics GitHub Repository](https://github.com/ultralytics)
        """
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
            resp (Response): API response data, containing paginated results and metadata.

        Returns:
            None

        Notes:
            This function updates the internal state of the PaginatedList instance, including the current list of
            results, total number of pages, and the record identifier for pagination. If the response contains no
            data, it resets the results and total pages to default values.

        References:
            [Requests Library](https://docs.python-requests.org/en/master/)
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
        Retrieves a list of items from the API using pagination.

        Args:
            page_size (int, optional): The number of items per page. Defaults to 10.
            last_record (str, optional): ID of the last record from the previous page.
            query (dict, optional): Additional query parameters for the API request.

        Returns:
            (Optional[Response]): Response object from the list request, or None if the request fails.

        Notes:
            This function utilizes the `requests` library to perform the API request and handles pagination
            parameters including page size and last record ID.

        References:
            - [requests library](https://docs.python-requests.org/en/master/)
            - [Math library in Python](https://docs.python.org/3/library/math.html)
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
