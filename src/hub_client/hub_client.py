from config import HUB_API_ROOT
from api_client import APIClient

from models import Models

def require_authentication(func):
    def wrapper(self, *args, **kwargs):
        if not self.authenticated:
            raise PermissionError("Access Denied: Authentication required.")
        return func(self, *args, **kwargs)
    return wrapper

class HUBClient:

    def __init__(self, credentials=None):
        self.api_client = APIClient(f"{HUB_API_ROOT}")
        self.authenticated = bool(credentials)
        if credentials:
            self.login(**credentials)

    def login(self, api_key=None, id_token=None, email=None, password=None):
        self.authenticated = True

    @require_authentication
    def models(self):
        return Models()