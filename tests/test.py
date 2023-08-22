from hub_client import HUBClient

# Authenticate with the server
# crednetials = {"api_key": "0cfff8f4e9357c3777c0871d35802915913c2f71c3"}
crednetials = {"email": "rick.sanchez@citadel.com", "password": "987654321"}
hub = HUBClient(crednetials)


# Initialise a datasets client
datasets = hub.datasets()
# Get Datasets list
response = datasets.list()
# Fetch a model
response = datasets.read("MODEL_ID")
# Update a model
# response = datasets.update("oNkgWRAp87DoD591yBtf", {"meta": {"name": "Hello"}})
# Soft delete a model
response = datasets.delete("MODEL_ID")
# Hard delete a model
response = datasets.delete("MODEL_ID", True)



# Initialise a projects client
projects = hub.projects()

# Get projects list
response = projects.list()
# Fetch a projects
response = projects.read("PROJECT_ID")
# Create a new projects
response = projects.create({"meta": {"name": "My favorite projects"}})
# Update a projects
response = projects.update("PROJECT_ID", {"meta": {"name": "Hello"}})
# Soft delete a projects
response = projects.delete("PROJECT_ID")
# Hard delete a projects
response = projects.delete("PROJECT_ID", True)


# Initialise a teams client
teams = hub.teams()
# Get Teams list
response = teams.list()
# Fetch a teams
response = teams.read("TEAMS_ID")
# Create a new teams
response = teams.create({"meta": {"name": "My favorite teams"}})
# Update a teams
response = teams.update("TEAMS_ID", {"meta": {"name": "Hello"}})
# Soft delete a teams
response = teams.delete("TEAMS_ID")
# Hard delete a teams
response = teams.delete("TEAMS_ID", True)


# Initialise a datasets client
datasets = hub.datasets()
# Get Datasets list
response = datasets.list()
# Fetch a dataset
response = datasets.read("DATASET_ID")
# Update a dataset
response = datasets.update("DATASET_ID", {"meta": {"name": "Hello"}})
# Soft delete a dataset
response = datasets.delete("DATASET_ID")
# Hard delete a dataset
response = datasets.delete("DATASET_ID", True)


# # Initialise a models client
models = hub.models()
# # Create a new model
response = models.create({"meta": {"name": "My favorite model"}})
# # Fetch a model
response = models.read("MODEL_ID")
# # Update a model
response = models.update("MODEL_ID", {"meta": {"name": "Hello"}})
# # Soft delete a model
response = models.delete("MODEL_ID")
# # Hard delete a model
response = models.delete("MODEL_ID", True)

# Upload a model
# response = models.upload("MODEL_ID", "CKPT", {"meta": "args"})
# # Predict with a model
# response = models.predict("MODEL_ID", "IMAGE", {"config": "args"})
# # Export a model
# response = models.export("MODEL_ID", {"format": "name"})


# Response is returned in this format
response = {
    "success": "true or false, for developers who are not familiar with status codes",
    "message": "Summary of result",
    "data": "Nested JSON with the result or an empty object if not needed.",
}

# Coming Soon

# Cloud training
# response = models.train("MODEL_ID", {"config": "args"})
