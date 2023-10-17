from hub_sdk import HUBClient

## Authenticate with the server
# crednetials = {"api_key": "99f3febd63071ad6c2d7fd17c1886cb01d8bded8ac"}
# crednetials = {"email": "rick.sanchez@citadel.com", "password": "987654321"}
# client = HUBClient(crednetials)

##################################
## Models Operations

# model_list = client.model_list(page_size=10, public=True)
# print(model_list.results) 
# model_list.next()
# model_list.previous()

## Project , Dataset ID for create New model
# data = {"meta": {"name": "sdk model"}, "projectId": "<project_id>", "datasetId": "<dataset_id>", "config":{"batchSize":"-1", "cache":"ram", "device":"name" , "epochs":"5", "imageSize":"640" ,"patience":"5"}}
# model = client.model()
# model.create_model(data)

## Updata model
# model = client.model("<Model ID>")
# print(model.update({"meta": {"name": "model Name"}}))

## delete model
# model = client.model("<Model ID>")
# model.delete()

# modelId = "URlpJ8JjvumpwMiLElSf" # Use Model ID to get model and upload model
# model = client.model(modelId)
# print(model.data)

# data =  {
#     1: '{"loss/1": 0.5, "accuracy/1": 0.85}',
#     2: '{"loss/2": 0.4, "accuracy/2": 0.88}',
#     3: '{"loss/3": 0.3, "accuracy/3": 0.90}',
# } 
# model.upload_metrics(data)  # upload metrics 

## Exports 
# modelId = "Epi7kTk7p2fQNHBGaPcD" # Use Model ID for export model
# model = client.model(modelId)
# print(model.data)
# model.export(format="pyTorch")  # upload export 


## Firebase-storage 
# data = {
#     "collection": "models",
#     "docId": "Epi7kTk7p2fQNHBGaPcD",
#     "object": "best"
# }
# storage = client.model(data)
# print(storage.get_dataset_url(data))

# model = client.model("<model ID>") # Model ID
# print(model.data)
# print(dataset.get_download_link("best"))

# Upload model
# modelID = "<MODEL ID>"
# model = client.model(datasetID)
# print("model Data", model.data)
# uploadmodel = model.upload_model(is_best= True, epoch=5, weights="example.pt")


###################################
## Dataset Operations
# create dataset

# data = {"meta":{"name":"my dataset"}, "filename": ""}
# dataset = client.dataset()
# dataset.create_dataset(data)

## get dataset by Id
# dataset = client.dataset('<Dataset ID>')
# print(dataset.data)

## Updata dataset
# dataset = client.dataset("<Dataset ID>")
# print(dataset.update({"meta": {"name": "dataset Name"}}))

## delete dataset
# dataset = client.dataset("<Dataset ID>")
# dataset.delete()

## List dataset
# dataset = client.dataset_list(page_size=1)
# print(dataset.results)
# dataset.next()
# dataset.previous()

# datasetID = "model ID" # Use Model ID to get model and upload model
# dataset = client.dataset(datasetID)
# print(dataset.data)
# print(dataset.get_download_link("archive"))

#  Upload Dataset

# datasetID = "<dataset ID>"
# dataset = client.dataset(datasetID)
# print("dataset Data", dataset.data)
# uploadDataset = dataset.upload_dataset(file="coco8.zip")

#####################################
## Project Operations
## create project
# data ={"meta":{"name":"my project"}} 
# project = client.project()
# project.create_project(data)

## get project
# project = client.project('<Project ID>')
# print(project.data)

## update project
# project = client.project('<Project ID>')
# print(project.update({"meta": {"name": "Project name update"}}))

## delete project 
# project = client.project("<Project ID>")
# print(project.delete())

## List Project
# projects = client.project_list(page_size=1, public=True)  
# print(projects.results)
# projects.next()
# projects.previous()


# projectID = "<Project ID>" # Use Model ID to get model and upload model
# project = client.project(projectID)
# print(project.data)
# project.upload_image(file = "project_image.jpeg")  # upload metrics 


#######################################
## Team Operations
# team = client.team({"meta":{"name":"my team"}}) # Create Teams 
# print(team.data)
# team = client.team('Teams ID')  # teams ID to data
# print(team.data)
# team.update({"meta": {"name": "Team Name update"}}) # for update teams
# team.delete() # for delete teams

# teams = client.team_list(page_size=1)   # teams list 
# print(teams.results)
# teams.next()
# teams.previous()




## Coming Soon

## Cloud training
# response = models.train("MODEL_ID", {"config": "args"})