# Model Management Operations

### Get Model by ID
This function lets you get a model by its specific ID. It sets up a model object with the given ID, enabling you to interact with and modify the model's data.

```python
model = client.model("<Model ID>")
print(model.data)
```

### Project and Dataset Check
This code snippet ensures the presence of both a project and a dataset by initializing their objects using their respective IDs. In case either of these IDs is not available, it raises an exception, as both are essential prerequisites for the creation of a model.
```python
project = client.project("<Project ID>")
dataset = client.dataset("<Dataset ID>")
if None in (project.id, dataset.id):
    raise "Available"
```
### Create New Model
This function sets up a fresh model with given details like name, project ID, dataset ID, and configuration options such as batch size, cache type, device, epochs, and image size. It then builds the model using the provided information.
```python
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

```python
model = client.model("<Model ID>")
model.update({"meta": {"name": "model Name"}})
```

### Delete Model
This function lets you erase a particular model by giving its ID. Use it carefully, as it permanently erases the model and its linked data.

```python
model = client.model("Model ID")
model.delete()
```

### Listing Models
This code snippet retrieves a list of projects using a specified page size. It displays the current page's results, advances to the next page, and prints those results. This cycle continues until all available projects are fetched. By setting *"public=True"* in the *model_list* arguments, it retrieves all public projects.

```python
model_list = client.model_list(page_size=10)
print("Current result:", model_list.results)
model_list.next()
print("Next page result:", model_list.results)
model_list.previous()
print("Previous page result:", model_list.results)
```

### Upload Metrics
You can provide the model's ID along with a metrics dictionary, typically containing loss and accuracy values for different training steps, as parameters for the function. This facilitates the ongoing monitoring and visualization of the model's training progress.

```python
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
This code exports a model in a chosen format, such as Tensorflow or PyTorch. You input the model's ID, and the function exports the model in the specified format, making it ready for deployment or in-depth analysis.

```python
modelId = "<Model ID>"
model = client.model(modelId)
model.export(format="pyTorch")
```

### Get URL form Storage
This function retrieves a URL for accessing the model's storage. It's useful when you need to access the model's data or artifacts stored in a remote location. The example provided download link of the model.

```python
modelId = "<Model ID>"
model = client.model(modelId)
model.get_download_link("best")
```

### Upload Model
The upload_model function uploads a model checkpoint specified by the given model_id. The is_best flag indicates if it's the best model. The epoch parameter denotes the training epoch. The model weights are provided via the "weights" file.

```python
model_id = "<Model ID>"
model = client.model(model_id)
model.upload_model(is_best=True, epoch="5", weights="<Weight File>")
```
