import json


def load_data(file_path):
    """
    Loads JSON data from a specified file path.

    Args:
        file_path (str): Path to the JSON file to be loaded.

    Returns:
        (dict | None): Parsed JSON data as a dictionary if the file is found, otherwise `None`.

    Example:
        ```python
        data = load_data("data.json")
        if data is not None:
            print("Loaded data:", data)
        ```

    Notes:
        If the file specified by `file_path` does not exist, the function will print an error message and return `None`.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None


class TestData:
    """
    A utility class for accessing various test datasets, including authentication, API, datasets, projects, and models
    data.

    This class provides class methods to fetch different categories of data from a JSON test dataset, aiding in unit testing
    and validation processes.

    Attributes:
        _data (dict | None): The loaded JSON data from 'tests/test_data/data.json'. If the file doesn't exist, it is `None`.

    Methods:
        get_auth_data: Loads and returns authentication data from the test dataset.
        get_api_data: Returns API data from the test dataset, including endpoints and keys.
        get_datasets_data: Returns datasets data from the test dataset, including details like names and sizes.
        get_projects_data: Fetches and returns projects data including names, ids, and creation dates from the test dataset.
        get_models_data: Returns models data including names, ids, and architecture details from the test dataset.

    Example:
        ```python
        auth_data = TestData.get_auth_data()
        print(auth_data)

        api_data = TestData.get_api_data()
        print(api_data)
        ```

    References:
        [JSON Data Interchange Format](https://www.json.org)
    """

    _data = load_data("tests/test_data/data.json")

    @classmethod
    def get_auth_data(cls):
        """
        Loads and returns authentication data from the test dataset.

        Returns:
            (dict | None): Authentication data if available, otherwise `None`.

        Note:
            The data is loaded from a predefined JSON file stored in the 'tests/test_data/data.json' path, which is
            expected to include keys relevant for authentication.

        Example:
            ```python
            auth_data = TestData.get_auth_data()
            if auth_data:
                print(auth_data['username'])
            ```

        References:
            [JSON module](https://docs.python.org/3/library/json.html)
        """
        return cls._data["auth_data"]

    @classmethod
    def get_api_data(cls):
        """
        Returns API data from the test dataset, including endpoints and keys.

        Args:
            None

        Returns:
            (dict): A dictionary containing API endpoint data with keys such as 'endpoints' and 'keys'.

        Example:
            ```python
            api_data = TestData.get_api_data()
            print(api_data["endpoints"])
            ```

        Notes:
            Ensure that 'tests/test_data/data.json' exists and contains valid JSON structure for proper functionality.
        """
        return cls._data["api_data"]

    @classmethod
    def get_datasets_data(cls):
        """
        Returns datasets data from the test dataset, including details like names and sizes.

        Args:
            None

        Returns:
            (dict): A dictionary containing datasets data with keys like 'name' and 'size'.

        Example:
            ```python
            datasets_data = TestData.get_datasets_data()
            print(datasets_data)
            ```
        """
        return cls._data["datasets_data"]

    @classmethod
    def get_projects_data(cls):
        """
        Fetches and returns projects data including names, ids, and creation dates from the test dataset.

        Args:
            None

        Returns:
            (dict): Projects data containing details such as names, ids, and creation dates.

        Example:
            ```python
            projects_data = TestData.get_projects_data()
            print(projects_data)
            ```

        References:
            [JSON Documentation](https://www.json.org/json-en.html)
        """
        return cls._data["projects_data"]

    @classmethod
    def get_models_data(cls):
        """
        Returns models data including names, ids, and architecture details from the test dataset.

        Args:
            None

        Returns:
            (dict): Dictionary containing models data from the test dataset, structured with keys such as names, ids,
                and architecture details.

        Example:
            ```python
            models_data = TestData.get_models_data()
            print(models_data)  # Outputs models data including names, ids, and architecture details
            ```
        """
        return cls._data["models_data"]
