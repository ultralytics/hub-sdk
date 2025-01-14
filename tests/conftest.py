# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

import pytest
import requests

from hub_sdk import HUBClient
from tests.features.object_manager import ObjectManager
from tests.test_data.data import TestData

fixture_scope = None
client: HUBClient


def pytest_addoption(parser):
    """
    Add a custom command-line option '--fixture_scope'.

    Usage:
    Run pytest with '--fixture_scope=function' to set the option to 'function'.
    """
    parser.addoption("--fixture_scope", action="store", default="class")


def determine_scope(fixture_name, config):
    """Determines fixture scope based on configuration."""
    global fixture_scope
    fixture_scope = config.getoption("--fixture_scope")
    return fixture_scope


@pytest.fixture(scope=determine_scope)
def setup(request):
    """
    Fixture to set up the test environment.

    This fixture initializes a test client with valid API key credentials
    and makes it available to the test cases.

    Args:
        request (FixtureRequest): The fixture request object.

    Returns:
        HUBClient: An instance of the HUBClient with initialized credentials.
    """
    global client

    # Obtain the valid API key
    api_key = TestData().get_auth_data()["valid_api_key"]

    # Set up the credentials with the API key
    credentials = {"api_key": api_key}

    # Initialize the HUBClient with the provided credentials
    client = HUBClient(credentials)

    # Make the HUBClient instance available to the test cases
    request.cls.client = client

    # Yield the HUBClient instance to the test cases
    yield client


@pytest.fixture(scope="module")
def data_for_test():
    """
    Fixture providing dynamic data for test cases.

    This fixture yields a dictionary containing information such as the model,
    dataset, and project with default values. The values can be modified within
    test cases, allowing the sharing of dynamic data between multiple test cases
    in the same module.

    Returns:
    dict: A dictionary containing dynamic data
    """
    yield {}


@pytest.fixture(scope="function")
def delete_test_model(request):
    """
    Fixture for deleting a test model after test execution.

    This fixture retrieves the test name and associated model_id from the test request to perform the deletion logic
    using the model_id.
    """
    yield
    test_name = request.node.name
    model_id_key = f"model_id_for_{test_name}"
    model_id = request.config.cache.get(model_id_key, None)

    if model_id is not None:
        page_object_manager = ObjectManager(client)
        model_page = page_object_manager.get_model()
        model_page.delete_model(model_id)


@pytest.fixture(scope="function")
def create_test_model(request):
    """
    Fixture for creating a test model before test execution.

    This fixture creates a new model using test data and sets the model_id in the cache for subsequent use during the
    test.
    """
    new_model_data = TestData().get_models_data()["new_model_data"]
    page_object_manager = ObjectManager(client)
    model_page = page_object_manager.get_model()

    # Create new model
    model_id = model_page.create_new_model(new_model_data)

    # Set the model_id in the request.config.cache
    test_name = request.node.name
    model_id_key = f"model_id_for_{test_name}"
    request.config.cache.set(model_id_key, model_id)
    yield


@pytest.fixture(scope="function")
def clear_export_model():
    """Pytest fixture to clear exports of a specific model after test execution."""
    yield
    model_id = TestData().get_models_data()["valid_model_ID"]
    host = TestData().get_api_data()["host"]
    url = f"{host}/qa/model/{model_id}/clear_exports"

    payload = {}
    headers = {"x-api-key": TestData().get_auth_data()["valid_api_key"]}
    requests.post(url=url, headers=headers, data=payload)


@pytest.fixture(scope="function")
def delete_test_dataset(request):
    """
    Fixture for deleting a test dataset after test execution.

    This fixture retrieves the test name and associated dataset_id from the test request to perform the deletion logic
    using the dataset_id.
    """
    yield
    test_name = request.node.name
    dataset_id_key = f"dataset_id_for_{test_name}"
    dataset_id = request.config.cache.get(dataset_id_key, None)

    if dataset_id is not None:
        page_object_manager = ObjectManager(client)
        dataset_page = page_object_manager.get_dataset()
        dataset_page.delete_dataset(dataset_id)


@pytest.fixture(scope="function")
def create_test_dataset(request):
    """
    Fixture for creating a test dataset before test execution.

    This fixture creates a new dataset using test data and sets the dataset_id in the cache for subsequent use during
    the test.
    """
    new_dataset_data = TestData().get_datasets_data()["new_dataset_data"]
    page_object_manager = ObjectManager(client)
    dataset_page = page_object_manager.get_dataset()

    # Create new dataset
    dataset_id = dataset_page.create_new_dataset(new_dataset_data)

    # Set the dataset_id in the request.config.cache
    test_name = request.node.name
    dataset_id_key = f"dataset_id_for_{test_name}"
    request.config.cache.set(dataset_id_key, dataset_id)
    yield


@pytest.fixture(scope="function")
def delete_test_project(request):
    """
    Fixture for deleting a test project after test execution.

    This fixture retrieves the test name and associated project_id from the test request to perform the deletion logic
    using the project_id.
    """
    yield
    test_name = request.node.name
    project_id_key = f"project_id_for_{test_name}"
    project_id = request.config.cache.get(project_id_key, None)

    if project_id is not None:
        page_object_manager = ObjectManager(client)
        project_page = page_object_manager.get_project()
        project_page.delete_project(project_id)


@pytest.fixture(scope="function")
def create_test_project(request):
    """
    Fixture for creating a test project before test execution.

    This fixture creates a new project using test data and sets the project_id in the cache for subsequent use during
    the test.
    """
    new_project_data = TestData().get_projects_data()["new_project_data"]
    page_object_manager = ObjectManager(client)
    project_page = page_object_manager.get_project()

    # Create new project
    project_id = project_page.create_new_project(new_project_data)

    # Set the project_id in the request.config.cache
    test_name = request.node.name
    project_id_key = f"project_id_for_{test_name}"
    request.config.cache.set(project_id_key, project_id)
    yield
