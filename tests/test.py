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


# model = client.model({"meta":{"name":"my Model"}})
# print(model.data)
# model = client.model("MODEL ID")
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

# Team Operations

# team = client.team({"meta":{"name":"my team"}})
# print(team.data)
# team = client.team('TEAM ID')
# print(team.data)
team = client.team("h5PPUBNkVJV8qqQQclfU")
print(team.delete())
# team = client.team('TEAM ID')
# print(team.data)
# team = client.team("PROJECT ID")
# print(team.update({"meta": {"name": "Team Name"}}))
# teams = client.team_list(page_size=1)
# print(teams.results)

# Project Operations

# project = client.project({"meta":{"name":"my project"}})
# print(project.data)
# project = client.project('PROJECT ID')
# print(project.data)
# project = client.project("PROJECT ID")
# print(project.delete)
# project = client.project("PROJECT ID")
# print(project.update({"meta": {"name": "Project Name"}}))
# projects = client.project_list(page_size=1)
# print(projects.results)

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
