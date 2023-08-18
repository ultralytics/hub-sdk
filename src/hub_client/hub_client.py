from .auth import Auth
from .models import Models
import os

def require_authentication(func):
    def wrapper(self, *args, **kwargs):
        if not self.authenticated:
            raise PermissionError("Access Denied: Authentication required.")
        return func(self, *args, **kwargs)
    return wrapper

class HUBClient(Auth):
    def __init__(self, credentials=None):
        self.authenticated = False
        if not credentials:
            self.api_key = os.environ.get("HUB_API_KEY")  # Safely retrieve the API key from an environment variable.
            credentials = {"api_key": self.api_key}

        self.login(**credentials)

    def login(self, api_key=None, id_token=None, email=None, password=None):
        
        self.id_token = id_token
        if self.api_key or self.id_token:
            self.authenticated = True
            # if self.authenticate():
            #     self.authenticated = True

        elif email and password:
            if self.authorize(email, password):
                self.authenticated = True  


    @require_authentication
    def models(self):
        return Models(self.get_auth_header())