---
comments: true
description: Explore comprehensive steps to manage, create, update, and deploy your ML models with Ultralytics HUB-SDK. Elevate your machine learning workflows.
keywords: Ultralytics, HUB-SDK, model management, machine learning, create model, update model, deploy model, ML workflow
---

# Ultralytics HUB-SDK Model Management Operations Guide

Welcome to the Ultralytics HUB-SDK Model Management documentation! Whether you're just getting started with managing machine learning models or you're a seasoned data scientist looking for specific operation instructions, you've come to the right place. Let's embark on a smooth journey through the HUB-SDK features, ensuring you gain the know-how to efficiently manage your models.

## Retrieve a Model by its Unique Identifier

In machine learning workflows, you often need to access a specific model. With Ultralytics HUB-SDK, fetching a model by its ID is a breeze. This essential function sets up a model object based on the provided unique identifier, granting you full access to the model's details and operations.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

model = client.model("<Model ID>")
print(model.data)  # Outputs the model's metadata and configuration
```

## Access Project and Dataset Prerequisites

Prior to model creation or training, ensuring the presence of both a project and a dataset is crucial. This straightforward code snippet helps you verify these components are available by initializing their objects. While utilizing a project and dataset for organizing model training is beneficial, it's important to note that it is not mandatory. If either ID is missing, the object data (`project.data`, `dataset.data`) will  be empty.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

project = client.project("<Project ID>")
dataset = client.dataset("<Dataset ID>")
```

## Create a New Model with Custom Configuration

Creating a new model tailored to your project requirements is made simple with this convenient function. Specify the model's name and associate it with your project and dataset. You can also customize configurations to fit your needs, such as setting the batch size or device, among others. Note that `projectId` and `datasetId` parameters are optional if you're not ready to tie the model to a project or dataset yet.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

data = {
    "meta": {"name": "sdk model"},  # Give your model a recognizable name
    "projectId": project.id,  # Associate with an existing project
    "datasetId": dataset.id,  # Associate with an existing dataset
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

As projects develop, you might need to update a model's metadata, such as renaming it for clarity. The SDK provides a method to refresh these details effortlessly, minimizing manual errors and saving you precious time.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

model = client.model("<Model ID>")
model.update({"meta": {"name": "Updated Model Name"}})  # Renames the specified model
```

## Delete a Model Safely

Deleting a model is irreversible, so this function should be used with caution. When you're sure you want to remove a model from the system, the following command will permanently delete the specified model, along with all its associated data.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

model = client.model("<Model ID>")
model.delete(hard=True)  # Permanently deletes the specified model
```
By default, the delete method performs a soft delete, marking the model as inactive without removing it permanently. If you want to perform a hard delete and remove the model along with its associated data permanently, you can pass the argument `hard=True` as shown in the example above. Exercise caution when using the hard delete option, as it is irreversible and results in the complete removal of the specified model from the system.

## Listing All Your Models with Pagination

Ultralytics HUB-SDK streamlines the task of fetching lists of models, while implementing pagination to efficiently navigate through potentially large collections of models. By customizing arguments such as `page_size`, you can tailor the output to your needs, including the ability to view both private and public projects.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

model_list = client.model_list(page_size=10)  # Fetches the first page with 10 models
print("Current result:", model_list.results)  # Displays the current page's models

model_list.next()  # Move to the next page of results
print("Next page result:", model_list.results)  # Displays the next page's models

model_list.previous()  # Return to the previous page of results
print("Previous page result:", model_list.results)  # Displays the previous page's models
```

## Upload and Visualize Training Metrics

To track and visualize your model's performance metrics throughout the training process, use this function to upload metrics such as loss and accuracy. This enables the continual monitoring of training progress and simplifies the analysis stage.

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

Exporting models for various purposes such as deployment or in-depth analysis has never been easier. Specify the format you require, and this function will prepare the model accordingly. Whether you need a Tensorflow or a PyTorch format, the SDK handles it seamlessly.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

model = client.model("<Model ID>")
model.export(format="pyTorch")  # Exports the model as a PyTorch file
```

## Retrieve a Direct Weight URL

Occasionally, you might require direct access to your model's remotely-stored artifacts. This convenient function provides a URL to access specific files like your best-performing model weights.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

model = client.model("<Model ID>")
weight_url = model.get_weights_url("best")  # or "last"
print("Weight URL link:", weight_url)  # Prints out the weight url link
```

## Upload a Model Checkpoint

Uploading a model checkpoint is made straightforward with the `upload_model` function. Simply indicate the significance of the checkpoint with the `is_best` flag and the training epoch for clarity.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

model = client.model("<Model ID>")
model.upload_model(is_best=True, epoch=5, weights="<Weight File>")  # Uploads the specified model checkpoint
```

In conclusion, Ultralytics HUB-SDK offers a comprehensive set of operations for effective model management, enabling you to focus on achieving the best results in your machine learning endeavors. Should you have any further questions or require assistance, please reach out to our welcoming community or support team. Happy modeling! 🚀
