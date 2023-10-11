from hub_sdk import HUBClient

## Authenticate with the server
# crednetials = {"api_key": "99f3febd63071ad6c2d7fd17c1886cb01d8bded8ac"}
# crednetials = {"email": "rick.sanchez@citadel.com", "password": "987654321"}
# client = HUBClient(crednetials)

## Models Operations

# model_list = client.model_list(page_size=10, public=True)  # Use client.ModelList to create an instance  # public True for Public data
# print("1: ", model_list.results) 
# model_list.next()    
# print("2: ", model_list.results)
# model_list.previous()
# print("previous: ", model_list.results)

# model = client.model("URlpJ8JjvumpwMiLElSf") # Model ID
# print(model.data)
# print(dataset.get_download_link("best"))

# datasetID = "3OwLTYXLUaeHVTudXRdO" # Use Model ID to get model and upload model
# dataset = client.dataset(datasetID)
# print(dataset.data)
# print(dataset.get_download_link("archive"))

## Project , Dataset ID for create New model
# data = {"meta": {"name": "sdk model"}, "projectId": "z8HsyRxDFqly8lANOiYb", "datasetId": "3OwLTYXLUaeHVTudXRdO", "config":{"batchSize":"-1", "cache":"ram", "device":"name" , "epochs":"5", "imageSize":"640" ,"patience":"5"}}
# model = client.model()
# model.create_model(data)


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


## Dataset Operations
## create dataset

# Upload model

# datasetID = "KUGRLIK8C4nytMcYNiW9"
# dataset = client.model(datasetID)
# print("dataset Data", dataset.data)
# uploadDataset = dataset.upload_model(is_best= True, epoch=5, weights="example.pt")


# Dataset Operations

#  Upload Dataset

# datasetID = "3OwLTYXLUaeHVTudXRdO"
# dataset = client.dataset(datasetID)
# print("dataset Data", dataset.data)
# uploadDataset = dataset.upload_dataset(file="coco8.zip")

#  Crud Operations

# data = {"meta":{"name":"my dataset"}, "filename": ""}
# dataset = client.dataset()
# dataset.create_dataset(data)

## get dataset by Id
# dataset = client.dataset('3OwLTYXLUaeHVTudXRdO')
# print(dataset.data)

## Updata dataset
# dataset = client.dataset("1jDR6r52XGWiRUBEstYw")
# print(dataset.update({"meta": {"name": "dataset Name"}}))

## delete dataset
# dataset = client.dataset("1jDR6r52XGWiRUBEstYw")
# dataset.delete()

## List dataset
# dataset = client.dataset_list(page_size=1)
# print(dataset.results)
# print("1: ", dataset.results)
# dataset.next()
# print("2: ", dataset.results)
# dataset.previous()
# print("previous: ", dataset.results)


## Team Operations

# team = client.team({"meta":{"name":"my team"}}) # Create Teams 
# print(team.data)
# team = client.team('Teams ID')  # teams ID to data
# print(team.data)
# team.update({"meta": {"name": "Team Name update"}}) # for update teams
# team.delete() # for delete teams

# teams = client.team_list(page_size=1)   # teams list 
# print(teams.results)
# print("1: ", teams.results)
# teams.next()
# print("2: ", teams.results)
# teams.previous()
# print("previous: ", teams.results)

## Project Operations
## create project
# data ={"meta":{"name":"my project"}} 
# project = client.project()
# project.create_project(data)

## get project
# project = client.project('arP1HAMED0tcz770vG5l')
# print(project.data)

## update project
# project = client.project('arP1HAMED0tcz770vG5l')
# print(project.update({"meta": {"name": "Project name update"}}))

## delete project 
# project = client.project("arP1HAMED0tcz770vG5l")
# print(project.delete())

## List Project
# projects = client.project_list(page_size=1, public=True)  
# print(projects.results)
# print("1" , projects.results)
# projects.next()
# print("2" , projects.results)
# projects.next()
# print("previouss" , projects.results)
# projects.previous()

## Coming Soon

## Cloud training
# response = models.train("MODEL_ID", {"config": "args"})