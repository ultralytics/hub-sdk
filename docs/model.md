---
comments: true
description: Explore comprehensive steps to manage, create, update, and deploy your ML models with Ultralytics HUB-SDK. Elevate your machine learning workflows.
keywords: Ultralytics, HUB-SDK, model management, machine learning, create model, update model, deploy model, ML workflow
---

# Ultralytics HUB-SDK Model Management

Welcome to the Ultralytics HUB-SDK Model Management documentation! Whether you're just getting started with managing machine learning models or you're a seasoned data scientist looking for specific operation instructions, you've come to the right place. This guide provides a smooth journey through the HUB-SDK features, ensuring you gain the know-how to efficiently manage your models.

## Retrieve a Model by its Unique Identifier

In machine learning workflows, accessing a specific model is a common requirement. With Ultralytics HUB-SDK, [fetching a model by its ID](https://docs.ultralytics.com/hub/sdk/model/#retrieve-a-model-by-its-unique-identifier) is straightforward. This function sets up a model object based on the provided unique identifier, granting you full access to the model's details and operations.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

model = client.model("<Model ID>")
print(model.data)  # Outputs the model's metadata and configuration
```

## Access Project and Dataset Prerequisites

Before creating or training a model, it's crucial to ensure that both a [project](https://docs.ultralytics.com/hub/sdk/project/) and a [dataset](https://docs.ultralytics.com/hub/sdk/dataset/) are present. The following code snippet helps verify these components by initializing their objects. While utilizing a project and dataset to organize model training is beneficial, it's not mandatory. If either ID is missing, the object data (`project.data`, `dataset.data`) will be empty.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

project = client.project("<Project ID>")
dataset = client.dataset("<Dataset ID>")
```

## Create a New Model with Custom Configuration

Creating a [new model](https://docs.ultralytics.com/hub/sdk/model/#create-a-new-model-with-custom-configuration) tailored to your project requirements is simple with this function. Specify the model's name and associate it with your project and dataset. You can also customize configurations, such as setting the batch size or device. Note that `projectId` and `datasetId` parameters are optional if you're not ready to tie the model to a project or dataset yet.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

data = {
    "meta": {"name": "sdk model"},  # Model name
    "projectId": project.id,  # Optional: Associate with an existing project
    "datasetId": dataset.id,  # Optional: Associate with an existing dataset
    "config": {  # Define hyperparameters and settings
        "batchSize": "-1",
        "cache": "ram",
        "device": "name",
        "epochs": "5",
        "imageSize": "640",
        "patience": "5",  # Stop training if validation doesn't improve
    },
}
model = client.model()
model.create_model(data)  # Creates the model with your specified details
```

## Update an Existing Model's Metadata or Config

As projects evolve, you might need to [update a model's metadata](https://docs.ultralytics.com/hub/sdk/model/#update-an-existing-models-metadata-or-config), such as renaming it for clarity. The SDK provides a method to refresh these details effortlessly, minimizing manual errors and saving time.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

model = client.model("<Model ID>")
model.update({"meta": {"name": "Updated Model Name"}})  # Renames the specified model
```

## Delete a Model Safely

Deleting a model is irreversible, so use this function with caution. When you're sure you want to [remove a model](https://docs.ultralytics.com/hub/sdk/model/#delete-a-model-safely) from the system, the following command will permanently delete the specified model, along with all its associated data.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

model = client.model("<Model ID>")
model.delete(hard=True)  # Permanently deletes the specified model
```

By default, the `delete` method performs a soft delete, marking the model as inactive without removing it permanently. If you want to perform a hard delete and remove the model along with its associated data permanently, pass the argument `hard=True` as shown above. Exercise caution when using the hard delete option, as it is irreversible.

## Listing All Your Models with Pagination

Ultralytics HUB-SDK streamlines fetching [lists of models](https://docs.ultralytics.com/hub/sdk/model/#listing-all-your-models-with-pagination), implementing pagination to efficiently navigate through potentially large collections. By customizing arguments such as `page_size`, you can tailor the output to your needs, including the ability to view both private and public projects.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

model_list = client.model_list(page_size=10)  # Fetches the first page with 10 models
print("Current result:", model_list.results)  # Displays the current page's models

model_list.next()  # Move to the next page
print("Next page result:", model_list.results)

model_list.previous()  # Return to the previous page
print("Previous page result:", model_list.results)
```

## Upload and Visualize Training Metrics

To track and visualize your [model's performance metrics](https://docs.ultralytics.com/hub/sdk/model/#upload-and-visualize-training-metrics) throughout the training process, use this function to upload metrics such as loss and accuracy. This enables the continual monitoring of training progress and simplifies the analysis stage.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

model = client.model("<Model ID>")

# Define your metrics structure. Keys are steps, and values are JSON strings of metrics.
data = {
    1: '{"loss/1": 0.5, "accuracy/1": 0.85}',
    2: '{"loss/2": 0.4, "accuracy/2": 0.88}',
    3: '{"loss/3": 0.3, "accuracy/3": 0.90}',
}

model.upload_metrics(data)  # Uploads the specified metrics to the model
```

## Export Your Model for Deployment or Analysis

[Exporting models](https://docs.ultralytics.com/hub/sdk/model/#export-your-model-for-deployment-or-analysis) for various purposes, such as deployment or in-depth analysis, is straightforward. Specify the format you require, and this function will prepare the model accordingly. Whether you need a TensorFlow or PyTorch format, the SDK handles it seamlessly.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

model = client.model("<Model ID>")
model.export(format="pyTorch")  # Exports the model as a PyTorch file
```

## Retrieve a Direct Weight URL

Occasionally, you might require direct access to your [model's remotely-stored artifacts](https://docs.ultralytics.com/hub/sdk/model/#retrieve-a-direct-weight-url). This function provides a URL to access specific files, like your best-performing model weights.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

model = client.model("<Model ID>")
weight_url = model.get_weights_url("best")  # or "last"
print("Weight URL link:", weight_url)
```

## Upload a Model Checkpoint

Uploading a [model checkpoint](https://docs.ultralytics.com/hub/sdk/reference/modules/models/#upload_model) is straightforward with the `upload_model` function. Indicate the significance of the checkpoint with the `is_best` flag and the training epoch for clarity.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

model = client.model("<Model ID>")
model.upload_model(is_best=True, epoch=5, weights="<Weight File>")  # Uploads the specified model checkpoint
```

## Conclusion

Ultralytics HUB-SDK offers a comprehensive set of operations for effective model management, enabling you to focus on achieving the best results in your machine learning endeavors. Should you have any further questions or require assistance, please reach out to our community or support team. Happy modeling! 🚀
