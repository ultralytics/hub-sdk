# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import json


def load_data(file_path):
    """Loads and returns JSON data from the specified file path, returning `None` if the file does not exist."""
    try:
        with open(file_path) as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None


class TestData:
    """
    Manages loading and retrieval of test dataset info for authentication, API, datasets, projects, and models.

    This class provides a centralized way to access various test data components through class methods. The data is
    loaded once from a JSON file and stored as a class variable.

    Attributes:
        _data (Dict): The loaded test data containing authentication, API, datasets, projects, and models information.

    Methods:
        get_auth_data: Retrieves authentication data.
        get_api_data: Retrieves API data including endpoints and keys.
        get_datasets_data: Retrieves datasets information.
        get_projects_data: Retrieves projects data.
        get_models_data: Retrieves models data.
    """

    _data = load_data("tests/test_data/data.json")

    @classmethod
    def get_auth_data(cls):
        """Loads and returns authentication data from the test dataset."""
        return cls._data["auth_data"]

    @classmethod
    def get_api_data(cls):
        """Returns API data from the test dataset, including endpoints and keys."""
        return cls._data["api_data"]

    @classmethod
    def get_datasets_data(cls):
        """Returns datasets data from the test dataset, including details like names and sizes."""
        return cls._data["datasets_data"]

    @classmethod
    def get_projects_data(cls):
        """Fetches and returns projects data including names, ids, and creation dates from the test dataset."""
        return cls._data["projects_data"]

    @classmethod
    def get_models_data(cls):
        """Returns models data including names, ids, and architecture details from the test dataset."""
        return cls._data["models_data"]
