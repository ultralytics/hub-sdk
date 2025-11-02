# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import pytest

from hub_sdk import HUBClient
from tests.test_data.data import TestData
from tests.utils.base_class import BaseClass


class TestAuth(BaseClass):
    """
    Class for testing user authentication using HUBClient with various credential methods.

    This test class verifies authentication functionality using different credential types including API keys and
    email/password combinations. It tests both valid and invalid authentication scenarios.

    Attributes:
        None

    Methods:
        test_auth_001: Test authentication with valid API key.
        test_auth_002: Test authentication with valid email and password.
        test_auth_003: Test authentication with invalid API key.
    """

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

        log.info("Using invalid API key")
        credentials = {"api_key": invalid_api_key}

        log.info("Creating HUBClient instance with provided credentials")
        client = HUBClient(credentials)

        authentication_status = client.authenticated
        log.info(f"Authentication status: {authentication_status}")
        assert not authentication_status, "Authentication succeeded with an invalid API key"
