from hub_client import HUBClient

# Authenticate with the server
# crednetials = {"api_key": "0cfff8f4e9357c3777c0871d35802915913c2f71c3"}
crednetials = {"email": "rick.sanchez@citadel.com", "password": "987654321"}
client = HUBClient(crednetials)

# Models Operations

# model_list = client.model_list(page_size=1)  # Use client.ModelList to create an instance
# print("1: ", model_list.results)
# model_list.next()
# print("2: ", model_list.results)
# model_list.previous()
# print("previous: ", model_list.results)



# Initialise a teams client
teams = hub.teams()
# Get Datasets list
response = teams.list()
# Fetch a teams
response = teams.read("TEAMS_ID")
# # Create a new teams
response = teams.create({"meta": {"name": "My favorite model"}})
# # Update a teams
response = teams.update("TEAMS_ID", {"meta": {"name": "Hello"}})
# # Soft delete a teams
response = teams.delete("TEAMS_ID")
# # Hard delete a teams
response = teams.delete("TEAMS_ID", True)


# Initialise a datasets client
datasets = hub.datasets()
# Get Datasets list
response = datasets.list()
# Fetch a model
response = datasets.read("DATASET_ID")
# Update a model
response = datasets.update("DATASET_ID", {"meta": {"name": "Hello"}})
# Soft delete a model
response = datasets.delete("DATASET_ID")
# Hard delete a model
response = datasets.delete("DATASET_ID", True)


# Initialise a projects client
projects = hub.projects()

# model = client.model("KUGRLIK8C4nytMcYNiW9")
# print(model.update({"meta": {"name": "Model Name"}}))
# model = client.model("MODEL ID")
# print(model.delete())
# model = client.model("model ID")
# print(model.update({"meta": {"name": "model Name"}}))


# Dataset Operations

# dataset = client.dataset({"meta":{"name":"my dataset"}})
# print(dataset.data)
# dataset = client.dataset('DATASET ID')
# print(dataset.data)
# dataset = client.dataset_list(page_size=1)
# print(dataset.results)
# dataset = client.dataset("DATASET ID")
# print(dataset.delete())
# dataset = client.dataset("DATASET ID")
# print(dataset.update({"meta": {"name": "dataset Name"}}))

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
