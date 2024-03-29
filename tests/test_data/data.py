import json


def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None


class TestData:
    _data = load_data("tests/test_data/data.json")

    @classmethod
    def get_auth_data(cls):
        return cls._data["auth_data"]

    @classmethod
    def get_api_data(cls):
        return cls._data["api_data"]

    @classmethod
    def get_datasets_data(cls):
        return cls._data["datasets_data"]

    @classmethod
    def get_projects_data(cls):
        return cls._data["projects_data"]

    @classmethod
    def get_models_data(cls):
        return cls._data["models_data"]
