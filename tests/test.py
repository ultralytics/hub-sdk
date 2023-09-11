from ultralytics_hub_sdk import HUBClient

# Authenticate with the server
crednetials = {"api_key": "0cfff8f4e9357c3777c0871d35802915913c2f71c3"}
# crednetials = {"email": "rick.sanchez@citadel.com", "password": "987654321"}
client = HUBClient(crednetials)

# Models Operations

model_list = client.model_list(page_size=10, public=True)  # Use client.ModelList to create an instance  # public True for Public data
print("1: ", model_list.results) 
model_list.next()    
print("2: ", model_list.results)
model_list.previous()
print("previous: ", model_list.results)

model = client.model("Model ID") # Model ID
print(model.data)


project = client.project("Project ID")  # Project ID
dataset = client.dataset("Dataset ID")  # Dataset ID
if None in (project.id, dataset.id):
    raise "Hello"

# Project , Dataset ID for create New model
data = client.model({"meta": {"name": "sdk model"}, "projectId": project.id, "datasetId": dataset.id, "config":{"batchSize":"-1", "cache":"ram", "device":"name" , "epochs":"5", "imageSize":"640" ,"patience":"5"}})
print(data.data)


modelId = "Model ID" # Use Model ID to get model and upload model
model = client.model(modelId)
print(model.data)

data =  {
    1: '{"loss/1": 0.5, "accuracy/1": 0.85}',
    2: '{"loss/2": 0.4, "accuracy/2": 0.88}',
    3: '{"loss/3": 0.3, "accuracy/3": 0.90}',
} 
model.upload_metrics(data)  # upload metrics 

if model:
    model.upload_model(5, "example.pt", is_best=True, map=1.0, final=False)  # upload model

model = client.model("Model ID") # Model ID for Update model
print(model.update({"meta": {"name": "Model Name"},"config":{"epochs":"1", "batchSize":"-1"}}))

model = client.model("Model ID") # Model ID for delete model
print(model.delete())


# Dataset Operations

dataset = client.dataset({"meta":{"name":"my dataset"}, "filename": "example.pt"})
print(dataset.data)
dataset = client.dataset('Dataset ID') # dataset ID to get dataset
print(dataset.data)
dataset.update({"meta": {"name": "dataset Name"}})  # for delete dataset
dataset.delete() # for delete dataset

dataset = client.dataset_list(page_size=1) # dataset list  # Public True for public dataset
print(dataset.results)
print("1: ", dataset.results)
dataset.next()
print("2: ", dataset.results)
dataset.previous()
print("previous: ", dataset.results)


# Team Operations

team = client.team({"meta":{"name":"my team"}}) # Create Teams 
print(team.data)
team = client.team('Teams ID')  # teams ID to data
print(team.data)
team.update({"meta": {"name": "Team Name update"}}) # for update teams
team.delete() # for delete teams

teams = client.team_list(page_size=1)   # teams list 
print(teams.results)
print("1: ", teams.results)
teams.next()
print("2: ", teams.results)
teams.previous()
print("previous: ", teams.results)

# Project Operations

project = client.project({"meta":{"name":"my project"}}) # set data to create the project 
print(project.data)
project = client.project('Project ID') # get project ID to get project
print(project.data)
project.update({"meta": {"name": "Project name update"}}) # for update project
project.delete() # for delete project

projects = client.project_list(page_size=1, public=True)  # dataset list  # Public True for public dataset
print(projects.results)
print("1" , projects.results)
projects.next()
print("2" , projects.results)
projects.next()
print("previouss" , projects.results)
projects.previous()


# Coming Soon

# Cloud training
# response = models.train("MODEL_ID", {"config": "args"})
