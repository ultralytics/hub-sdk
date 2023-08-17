from hub_client import HUBClient

# Authenticate with the server
# crednetials = {"api_key": "1234567890"}
crednetials = {"email": "rick.sanchez@citadel.com", "password": "987654321"}
hub = HUBClient(crednetials)

# Initialise a models client
models = hub.models()
# Create a new model
response = models.create({"meta": {"name": "My favorite model"}})
# Fetch a model
response = models.read("MODEL_ID")
# Update a model
response = models.update("MODEL_ID", {"meta": {"name": "Hello"}})
# Soft delete a model
response = models.delete("MODEL_ID")
# Hard delete a model
response = models.delete("MODEL_ID", True)

# Upload a model
response = models.upload("MODEL_ID", "CKPT", {"meta": "args"})
# Predict with a model
response = models.predict("MODEL_ID", "IMAGE", {"config": "args"})
# Export a model
response = models.export("MODEL_ID", {"format": "name"})


# Response is returned in this format
response = {
    "success": "true or false, for developers who are not familiar with status codes",
    "message": "Summary of result",
    "data": "Nested JSON with the result or an empty object if not needed.",
}

# Coming Soon

# Cloud training
# response = models.train("MODEL_ID", {"config": "args"})
