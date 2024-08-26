import pytest
from hub_sdk import HUBClient

from tests.test_data.data import TestData
from tests.utils.base_class import BaseClass


class TestAuth(BaseClass):
    """Class for testing user authentication using HUBClient with various credential methods."""

    @pytest.mark.smoke
    def test_auth_001(self):
        """Verify if the user authenticates successfully using an API key."""
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
        """Verify if the user authenticates successfully using Email/Password."""
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
        """Verify an error is raised during initialization with an incorrect API key."""
        log = self.get_logger()
        invalid_api_key = TestData().get_auth_data()["invalid_api_key"]

        log.info(f"Using invalid API key: {invalid_api_key}")
        credentials = {"api_key": invalid_api_key}

        log.info("Creating HUBClient instance with provided credentials")
        client = HUBClient(credentials)

        authentication_status = client.authenticated
        log.info(f"Authentication status: {authentication_status}")
        assert not authentication_status, "Authentication succeeded with an invalid API key"
