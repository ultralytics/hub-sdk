import pytest
from hub_sdk import HUBClient

from tests.test_data.data import TestData
from tests.utils.base_class import BaseClass


class TestAuth(BaseClass):
    """
    TestAuth class for verifying user authentication using different methods.

    This class contains test methods for validating user authentication through API key and Email/Password mechanisms using
    the HUBClient.

    Methods:
        test_auth_001: Verifies user authentication using a valid API key.
        test_auth_002: Verifies user authentication using Email/Password (currently skipped as feature is not implemented).
        test_auth_003: Checks if an error is raised with an incorrect API key.

    Example:
        ```python
        test_instance = TestAuth()
        test_instance.test_auth_001()  # Checks authentication with a valid API key
        test_instance.test_auth_003()  # Checks handling of an invalid API key
        ```

    References:
        - [pytest Documentation](https://docs.pytest.org/en/latest/)
    """

    @pytest.mark.smoke
    def test_auth_001(self):
        """
        Verify if the user authenticates successfully using an API key.

        Args:
            None

        Returns:
            (None): This function does not return a value. It performs an assertion within the test case.

        Notes:
            This function is a pytest test case and is intended to be run within the pytest framework.

        References:
            [PyTest Documentation](https://docs.pytest.org/)
            [hub_sdk Documentation](https://your-hub-sdk-url/documentation)
        """

        log = self.get_logger()
        valid_api_key = TestData().get_auth_data()["valid_api_key"]

        credentials = {"api_key": valid_api_key}
        log.info("Creating HUBClient instance with provided credentials")
        client = HUBClient(credentials)

        authentication_status = client.authenticated
        log.info(f"Authentication status: {authentication_status}")
        assert authentication_status, "Client authentication failed"

    @pytest.mark.skip(reason="Feature is not implemented yet")
    @pytest.mark.smoke
    def test_auth_002(self):
        """
        Verifies if the user authenticates successfully using Email/Password.

        Args:
            credentials (dict): User credentials containing 'email' and 'password' as keys with respective values.

        Returns:
            (bool): True if authentication is successful, False otherwise.

        Example:
            ```python
            email = "user@example.com"
            password = "securepassword123"
            credentials = {"email": email, "password": password}
            client = HUBClient(credentials)
            assert client.authenticated
            ```

        Notes:
            This function currently skips execution as the feature is not yet implemented.

        References:
            [pytest.mark.skip documentation](https://docs.pytest.org/en/stable/skipping.html#skip-mark-a-test-function-to-be-skipped)
        """

        log = self.get_logger()
        email = TestData().get_auth_data()["valid_credentials"]["email"]
        password = TestData().get_auth_data()["valid_credentials"]["password"]

        log.info(f"Using Email: {email}")
        credentials = {"email": email, "password": password}

        log.info("Creating HUBClient instance with provided credentials")
        client = HUBClient(credentials)

        authentication_status = client.authenticated
        log.info(f"Authentication status: {authentication_status}")
        assert authentication_status, "Client authentication failed"

    @pytest.mark.smoke
    def test_auth_003(self):
        """
        Verify an error is raised during initialization with an incorrect API key.

        Args:
            None

        Returns:
            None

        Example:
            ```python
            test_auth_instance = TestAuth()
            test_auth_instance.test_auth_003()
            ```

        Notes:
            This test is part of the smoke test suite and checks if client initialization appropriately handles an invalid
            API key scenario. It is critical to ensure that the system does not authenticate with incorrect credentials and
            raises the appropriate error for further handling in applications relying on authenticated sessions.

        References:
            - [PyTest Documentation](https://docs.pytest.org/en/6.2.x/)
        """

        log = self.get_logger()
        invalid_api_key = TestData().get_auth_data()["invalid_api_key"]

        log.info(f"Using invalid API key: {invalid_api_key}")
        credentials = {"api_key": invalid_api_key}

        log.info("Creating HUBClient instance with provided credentials")
        client = HUBClient(credentials)

        authentication_status = client.authenticated
        log.info(f"Authentication status: {authentication_status}")
        assert not authentication_status, "Authentication succeeded with an invalid API key"
