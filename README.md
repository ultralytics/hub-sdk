# Ultralytics HUBClient SDK

**Local setup:**

Create virtual env

    pip3 install venv
    python3 -m venv venv
    source venv/bin/activate 

Build hub_client SDK

    python3 -m build
Install SDK

    pip3 install dist/hub_client-0.0.1.tar.gz


**Usage:**

```python

  

from hub_client import HUBClient
hub = HUBClient()
hub.login(api_key="API_KEY") #id_token, email, password
model = hub.model()

response = model.create()

response = model.read('MODEL_ID')

response = model.update('MODEL_ID', {"data":data})

response = model.delete('MODEL_ID')

response = model.list()

  
```