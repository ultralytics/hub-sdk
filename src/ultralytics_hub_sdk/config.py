import os

HUB_API_ROOT = os.environ.get('ULTRALYTICS_HUB_API', 'https://api.ultralytics.com')
HUB_WEB_ROOT = os.environ.get('ULTRALYTICS_HUB_WEB', 'https://hub.ultralytics.com')
HUB_FUNCTIONS_ROOT = os.environ.get('ULTRALYTICS_HUB_FUNCTIONS', 'https://europe-west1-ultralytics-hub-staging.cloudfunctions.net/')
FIREBASE_AUTH_URL = os.environ.get('FIREBASE_AUTH_URL', 'http://localhost:9099/identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyDlTep-ubgWoafviJJneFL35raoJjWFnOw')
