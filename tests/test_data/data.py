import json


def load_data(file_path):
    """Loads and returns JSON data from the specified file path, returning `None` if the file does not exist."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None


class TestData:
    """Manages and provides access to test dataset sections for authentication, API, projects, models, and datasets."""

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
