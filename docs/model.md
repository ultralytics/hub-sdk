# Model Management Operations

### Get Model by ID

This function allows you to retrieve a model by its unique identifier (ID). It initializes a model object using the provided model ID and allows you to access and manipulate the model's data.

```sh
model = client.model("<Model ID>")
print(model.data)
```

### Project and Dataset Check

This code snippet checks whether both a project and a dataset exist based on their respective IDs. It initializes project and dataset objects using their IDs and raises an exception if either of them is not available.

```sh
project = client.project("<Project ID>")
dataset = client.dataset("<Dataset ID>")
if None in (project.id, dataset.id):
    raise "Available"
```

### Create New Model

This function creates a new model with specified parameters and configurations. It takes in data including the model's name, project ID, dataset ID, and configuration settings such as batch size, cache type, device, number of epochs, and image size. It then creates the model using the provided data.

```sh
data = {
    "meta": {"name": "sdk model"},
    "projectId": project.id,
    "datasetId": dataset.id,
    "config": {
        "batchSize": "-1",
        "cache": "ram",
        "device": "name",
        "epochs": "5",
        "imageSize": "640",
        "patience": "5"
    }
}
model = client.model()
model.create_model(data)
```

### Update Model

This code demonstrates how to update the metadata of an existing model. You can change attributes like the model's name by specifying the model's ID and providing updated metadata.

```sh
model = client.model("<Model ID>")
model.update({"meta": {"name": "model Name"}})
```

### Delete Model

This function allows you to delete a specific model by providing its ID. Be cautious when using this function, as it permanently removes the model and its associated data.

```sh
model = client.model("Model ID")
model.delete()
```

### Listing Public Models

This code snippet fetches a list of public models, typically with a specified page size. It prints the results of the current page, moves to the next page, and prints those results as well. This process can be repeated until you've retrieved all the available public models.

```sh
model_list = client.model_list(page_size=10, public=True)
print("First: ", model_list.results)
model_list.next()
print("Next: ", model_list.results)
model_list.previous()
print("Previous: ", model_list.results)
```

### Upload Metrics

Here, you can upload training metrics for a specific model. The function takes the model's ID and a dictionary of metrics data, typically containing loss and accuracy values for different training iterations. This helps in tracking and visualizing the model's training progress.

```sh
modelId = "<Model ID>"
model = client.model(modelId)
data = {
    1: '{"loss/1": 0.5, "accuracy/1": 0.85}',
    2: '{"loss/2": 0.4, "accuracy/2": 0.88}',
    3: '{"loss/3": 0.3, "accuracy/3": 0.90}',
}
model.upload_metrics(data)
```

### Export Model

This code exports a model in a specified format, which is PyTorch in this case. You provide the model's ID, and the function exports the model in the requested format, making it suitable for deployment or further analysis.

```sh
modelId = "<Model ID>"
model = client.model(modelId)
print(model.data)
model.export(format="pyTorch")
```

### Get URL form Storage

This function retrieves a URL for accessing the model's storage. It's useful when you need to access the model's data or artifacts stored in a remote location. The example provided download link of the model.

```sh
modelId = "<Model ID>"
model = client.model(modelId)
print(model.data)
model.get_download_link("best")
```

### Upload Model

The upload_model function uploads a model checkpoint specified by the given model_id. The is_best flag indicates if it's the best model. The epoch parameter denotes the training epoch. The model weights are provided via the "weights" file.

```sh
model_id = "<Model ID>"
model = client.model(model_id)
model.upload_model(is_best=True, epoch="5", weights="<Weight File>")
```
