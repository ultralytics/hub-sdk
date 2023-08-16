from config import HUB_API_ROOT
from api_client import APIClient

class Auth:
    def __init__(self):
        self.get_auth_header = None

        
    def authenticate(self) -> bool:
        """
        Attempt to authenticate with the server using either id_token or API key.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        try:
            header = self.get_auth_header()
            if header:
                r = requests.post(f"{HUB_API_ROOT}/v1/auth", headers=header)
                if not r.json().get("success", False):
                    raise ConnectionError("Unable to authenticate.")
                return True
            raise ConnectionError("User has not authenticated locally.")
        except ConnectionError:
            self.id_token = self.api_key = False  # reset invalid
            LOGGER.warning(f"{PREFIX}Invalid API key ⚠️")
            return False
    
    def get_auth_header(self):
        """
        Get the authentication header for making API requests.

        Returns:
            (dict): The authentication header if id_token or API key is set, None otherwise.
        """
        if self.id_token:
            return {'authorization': f'Bearer {self.id_token}'}
        elif self.api_key:
            return {'x-api-key': self.api_key}
        else:
            return None

    def get_state(self) -> bool:
        """
        Get the authentication state.

        Returns:
            bool: True if either id_token or API key is set, False otherwise.
        """
        return self.id_token or self.api_key

    def set_api_key(self, key: str):
        """
        Set the API key for authentication.

        Args:
            key (str): The API key string.
        """
        self.api_key = key
