from ultralytics_hub_sdk import HUBClient

# Authenticate with the server
crednetials = {"api_key": "0cfff8f4e9357c3777c0871d35802915913c2f71c3"}
# crednetials = {"email": "rick.sanchez@citadel.com", "password": "987654321"}
client = HUBClient(crednetials)

# Models Operations

# model_list = client.model_list(page_size=1, public=True)  # Use client.ModelList to create an instance
# print("1: ", model_list.results)
# model_list.next()
# print("2: ", model_list.results)
# model_list.previous()
# print("previous: ", model_list.results)

# file_content = "This is some sample content."
# file_obj = io.StringIO(file_content)

# model = client.model({"meta":{"name":"my Model"}})
# print(model.data)


# model = client.model("0qHCVgqoN0ismVUArqJr")
# print(model.data)


# project = client.project("WpUYWRSC0Aw9HARoHOiy")
# dataset = client.dataset("3OwLTYXLUaeHVTudXRdO")
# if None in (project.id, dataset.id):
#     raise "Hello"


# modelId = "KUGRLIK8C4nytMcYNiW9"
# data = {"meta": {"name": "sdk model"}, "projectId": project.id, "datasetId": dataset.id, "config":{"batchSize":"-1", "cache":"ram", "device":"name" , "epochs":"5", "imageSize":"640" ,"patience":"5"}}
# model = client.model(modelId)
# print(model.data)
# if model:
#     model.upload_model(5, "example.pt", is_best=True, map=1.0, final=False)
# data =  {
#     1: '{"loss/1": 0.5, "accuracy/1": 0.85}',
#     2: '{"loss/2": 0.4, "accuracy/2": 0.88}',
#     3: '{"loss/3": 0.3, "accuracy/3": 0.90}',
# }
# model.upload_metrics(data)

# model = client.model("vlbuLVMJDQjTHe8eNixh")
# model.upload_model(5, "example.pt")
# model.start_heartbeat()
# model.stop_heartbeat()

# model = client.model("vlbuLVMJDQjTHe8eNixh")
# model.start_heartbeat()curl -X POST -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'Content-Length: 164' -H 'Content-Type: application/json' -H 'User-Agent: python-requests/2.31.0' -H 'x-api-key: 0cfff8f4e9357c3777c0871d35802915913c2f71c3' -d '{"metrics": {"1": "{\"loss\": 0.5, \"accuracy\": 0.85}", "2": "{\"loss\": 0.4, \"accuracy\": 0.88}", "3": "{\"loss\": 0.3, \"accuracy\": 0.90}"}, "type": "metrics"}' http://127.0.0.1:8000/v1/models/TezGen9ctrS07ncptnH4
# model.stop_heartbeat()

# model = client.model("vQ8xFOC1nQdUSr1Be2bK")
# print(model.update({"meta": {"name": "Model Name"},"config":{"epochs":"1", "batchSize":"-1"}}))

# model = client.model("p5p3YkTZMKBCTmcatQCl")
# print(model.delete())


# Dataset Operations

# dataset = client.dataset({"meta":{"name":"my dataset"}, "filename": "example.pt"})
# print(dataset.data)
# dataset = client.dataset('tk94Drp8DZGvrb1C8RO7')
# print(dataset.data)
# dataset = client.dataset("tk94Drp8DZGvrb1C8RO7")
# print(dataset.delete())
# dataset = client.dataset("tk94Drp8DZGvrb1C8RO7")
# print(dataset.update({"meta": {"name": "dataset Name"}}))

# dataset = client.dataset_list(page_size=1)
# print(dataset.results)
# print("1: ", dataset.results)
# dataset.next()
# print("2: ", dataset.results)
# dataset.previous()
# print("previous: ", dataset.results)


# Team Operations

# team = client.team({"meta":{"name":"my team"}})
# print(team.data)
# team = client.team('39s5eVtqBfAF0G6EsEeD')
# print(team.data)
# team = client.team("39s5eVtqBfAF0G6EsEeD")
# print(team.delete())
# team = client.team("39s5eVtqBfAF0G6EsEeD")
# print(team.update({"meta": {"name": "Team Name update"}}))

teams = client.team_list(page_size=1)
print(teams.results)
# print("1: ", teams.results)
# teams.next()
# print("2: ", teams.results)
# teams.previous()
# print("previous: ", teams.results)

# Project Operations

# project = client.project({"meta":{"name":"my project"}})
# print(project.data)
# project = client.project('sNDD4IRxYQkCigsPlw8N')
# print(project.data)
# project = client.project('sNDD4IRxYQkCigsPlw8N')
# print(project.update({"meta": {"name": "Project name update"}}))
# project = client.project("sNDD4IRxYQkCigsPlw8N")      
# print(project.delete())

# projects = client.project_list(page_size=1, public=True)  
# print(projects.results)
# print("1" , projects.results)
# projects.next()
# print("2" , projects.results)
# projects.next()
# print("previouss" , projects.results)
# projects.previous()


# Upload a model
# response = models.upload("MODEL_ID", "CKPT", {"meta": "args"})
# # Predict with a model
# response = models.predict("MODEL_ID", "IMAGE", {"config": "args"})
# # Export a model
# response = models.export("MODEL_ID", {"format": "name"})


# Response is returned in this format
# response = {
#     "success": "true or false, for developers who are not familiar with status codes",
#     "message": "Summary of result",
#     "data": "Nested JSON with the result or an empty object if not needed.",
# }

# Coming Soon

# Cloud training
# response = models.train("MODEL_ID", {"config": "args"})
