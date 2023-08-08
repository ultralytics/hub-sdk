# Ultralytics HUB SDK

Usage:
```python

from hub import HUB

hub = HUB()

hub.login(api_key="API_KEY") #id_token, email, password

model = hub.model()

response = model.create()
response = model.read('MODEL_ID')
response = model.update('MODEL_ID', {"data":data})
response = model.delete('MODEL_ID')
response = model.list()

```