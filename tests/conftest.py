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

    Args:
        parser (pytest.Parser): The parser object that manages command-line options and ini-file values.

    Returns:
        None

    Example:
        ```python
        # Run pytest with the custom option:
        $ pytest --fixture_scope=function
        ```

    References:
        [pytest documentation](https://docs.pytest.org/en/stable/writing_plugins.html#_pytest.hookspec.pytest_addoption)
    """
    parser.addoption("--fixture_scope", action="store", default="class")


def determine_scope(fixture_name, config):
    """
    Determines the scope of a pytest fixture based on the provided configuration.

    Args:
        fixture_name (str): The name of the fixture whose scope is being determined.
        config (pytest.Config): The pytest configuration object, which allows access to command-line options.

    Returns:
        None: This function does not return a value; it sets the global variable `fixture_scope` based on the
            configuration options.

    Notes:
        The function reads the scope from the pytest configuration options, which can be set via the
        '--fixture_scope' command-line argument when running tests with pytest.

    Example:
        ```python
        def pytest_addoption(parser):
            parser.addoption("--fixture_scope", action="store", default="class")

        def determine_scope(fixture_name, config):
            global fixture_scope
            fixture_scope = config.getoption("--fixture_scope")
        ```

    References:
        [pytest Command line options](https://docs.pytest.org/en/stable/reference.html#command-line-options)
    """
    global fixture_scope
    fixture_scope = config.getoption("--fixture_scope")
    return fixture_scope


@pytest.fixture(scope=determine_scope)
def setup(request):
    """
    Sets up the test environment for pytest, initializing a test client with valid API key credentials.

    Args:
        request (FixtureRequest): The fixture request object providing context for the fixture.

    Returns:
        (HUBClient): An instance of the HUBClient with initialized credentials.

    Example:
        ```python
        def test_example(setup):
            client = setup
            assert client is not None
        ```
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

    This fixture yields a dictionary containing information such as the model, dataset, and project with default values.
    The values can be modified within test cases, allowing the sharing of dynamic data between multiple test cases in
    the same module.

    Returns:
        (dict): A dictionary containing dynamic data.

    Example:
        ```python
        def test_example(data_for_test):
            data = data_for_test
            data['model'] = 'new_model'
            assert data['model'] == 'new_model'
        ```
    """

    yield {}


@pytest.fixture(scope="function")
def delete_test_model(request):
    """
    Deletes a test model after test execution.

    Args:
        request (FixtureRequest): The fixture request object, providing context for the test being executed.

    Returns:
        None

    Example:
        ```python
        def test_model_deletion(setup, delete_test_model):
            # Test code here
        ```
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
    Creates a test model before test execution.

    Args:
        request (FixtureRequest): The fixture request object used to interact with the test infrastructure.

    Returns:
        (None): This fixture does not return any data; it sets up the test environment.

    Notes:
        This fixture uses test data to create a new model before executing a test. The model ID is stored in the cache
        and can be retrieved using the test name.

    Example:
        ```python
        def test_example(create_test_model):
            # Access the created model through the fixture
            pass
        ```
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
    """
    Clears all exports of a specific model after test execution.

    Args:
        None

    Returns:
        None

    Notes:
        This function is used as a pytest fixture with a function scope, meaning it runs after each test function
        where it is used.

    References:
        - [pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
        - [requests Library](https://docs.python-requests.org/en/latest/)

    Example:
        ```python
        @pytest.mark.usefixtures("clear_export_model")
        def test_something():
            # test logic here
        ```
    """
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
    Deletes a test dataset after test execution.

    Args:
        request (FixtureRequest): The pytest fixture request object containing test context and configuration data.

    Returns:
        None

    Example:
        ```python
        def test_example(delete_test_dataset):
            # Your test code here
        ```

    Notes:
        - This function is intended for use as a pytest fixture.
        - It retrieves the test name and associated `dataset_id` from the pytest request object and performs the deletion
          using the `dataset_id`.
        - The deletion logic is handled by the `ObjectManager` class.
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
    Creates a test dataset before executing a test.

    Args:
        request (FixtureRequest): The fixture request object containing metadata about the test being executed.

    Returns:
        (None)

    Example:
        ```python
        def test_dataset_creation(create_test_dataset):
            assert create_test_dataset is not None
        ```
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
    Deletes a test project after test execution.

    Args:
        request (FixtureRequest): The fixture request object containing test specific information.

    Returns:
        None

    Notes:
        - This fixture retrieves the test name and associated project_id from the test request to perform the deletion logic
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
    Creates a new test project before test execution and caches its ID for subsequent use during the test.

    Args:
        request (FixtureRequest): Pytest fixture request object which provides access to the requesting test context.

    Returns:
        None

    Example:
        ```python
        def test_example(create_test_project):
            # Use the created test project within your test case
            project_id = request.config.cache.get(f"project_id_for_{request.node.name}")
            assert project_id is not None
        ```
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
