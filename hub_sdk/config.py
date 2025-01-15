# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import os

HUB_API_ROOT = os.environ.get("ULTRALYTICS_HUB_API", "https://api.ultralytics.com")
HUB_WEB_ROOT = os.environ.get("ULTRALYTICS_HUB_WEB", "https://hub.ultralytics.com")
FIREBASE_AUTH_URL = os.environ.get(
    "ULTRALYTICS_FIREBASE_AUTH_URL",
    "http://localhost:9099/identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyDlTep"
    "-ubgWoafviJJneFL35raoJjWFnOw",
)
HUB_FUNCTIONS_ROOT = f"{HUB_API_ROOT}"

HUB_EXCEPTIONS = os.getenv("ULTRALYTICS_HUB_EXCEPTIONS", "true").lower() == "true"

# Prefix to be used for console printouts
PREFIX = "Ultralytics HUB-SDK:"
