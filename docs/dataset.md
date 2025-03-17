---
comments: true
description: Learn how to manage datasets efficiently in Python using the Ultralytics HUB-SDK. Get, create, update, delete, list, and upload datasets easily.
keywords: Ultralytics, HUB-SDK, dataset management, Python, get dataset, create dataset, update dataset, delete dataset, list datasets, upload dataset, machine learning
---

# Dataset Management with Ultralytics HUB-SDK

Welcome to the Ultralytics HUB-SDK Dataset Management documentation! 👋

Efficient [dataset management](https://www.ultralytics.com/glossary/data-preprocessing) is crucial in machine learning. Whether you're a seasoned data scientist or a beginner, knowing how to handle dataset operations can streamline your workflow. This page covers the basics of performing operations on datasets using the [Ultralytics HUB](https://www.ultralytics.com/hub)-SDK in Python. The examples provided illustrate how to get, create, update, delete, and list datasets, and also how to get a URL for dataset access and upload datasets.

Let's dive in! 🚀

## Get a Dataset by ID

To fetch a specific dataset rapidly using its unique ID, use the code snippet below. This allows you to access essential information, including its data.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

# Fetch a dataset by ID
dataset = client.dataset("<Dataset ID>")  # Replace with your actual Dataset ID
print(dataset.data)  # This prints the dataset information
```

For more details on the `Datasets` class and its methods, see the [Reference for `hub_sdk/modules/datasets.py`](https://docs.ultralytics.com/hub/sdk/reference/modules/datasets/).

## Create a Dataset

To create a fresh dataset, define a friendly name for your dataset and use the `create_dataset` method as shown below:

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

# Define your dataset properties
data = {"meta": {"name": "My Dataset"}}  # Replace 'My Dataset' with your desired dataset name

# Create the dataset
dataset = client.dataset()
dataset.create_dataset(data)
print("Dataset created successfully!")
```

See the [`create_dataset`](https://docs.ultralytics.com/hub/sdk/reference/modules/datasets/#hub_sdk.modules.datasets.Datasets.create_dataset) method in the API reference for further information.

## Update a Dataset

As projects evolve, you may need to modify your dataset's metadata. This is as simple as running the following code with the new details:

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

# Obtain the dataset
dataset = client.dataset("<Dataset ID>")  # Insert the correct Dataset ID

# Update the dataset's metadata
dataset.update({"meta": {"name": "Updated Name"}})  # Modify 'Updated Name' as required
print("Dataset updated with new information.")
```

The [`update`](https://docs.ultralytics.com/hub/sdk/reference/modules/datasets/#hub_sdk.modules.datasets.Datasets.update) method provides more details on updating datasets.

## Delete a Dataset

To remove a dataset, whether to declutter your workspace or because it's no longer needed, you can permanently delete it by invoking the `delete` method:

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

# Select the dataset by its ID
dataset = client.dataset("<Dataset ID>")  # Ensure the Dataset ID is specified

# Delete the dataset
dataset.delete()
print("Dataset has been deleted.")
```

For more on deletion options, including hard deletes, see the [`delete`](https://docs.ultralytics.com/hub/sdk/reference/modules/datasets/#hub_sdk.modules.datasets.Datasets.delete) method documentation.

## List Datasets

To browse through your datasets, list all your datasets with pagination. This is helpful when dealing with a large number of datasets.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

# Retrieve the first page of datasets
datasets = client.dataset_list(page_size=10)
print("Current dataset:", datasets.results)  # Show the datasets on the current page

# Move to the next page and show results
datasets.next()
print("Next page result:", datasets.results)

# Go back to the previous page
datasets.previous()
print("Previous page result:", datasets.results)
```

The [`DatasetList`](https://docs.ultralytics.com/hub/sdk/reference/modules/datasets/#hub_sdk.modules.datasets.DatasetList) class provides more details on listing and paginating datasets.

## Get URL from Storage

This function fetches a URL for dataset storage access, making it easy to download dataset files or artifacts stored remotely.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

# Define the dataset ID for which you want a download link
dataset = client.dataset("<Dataset ID>")  # Replace Dataset ID with the actual dataset ID

# Retrieve the URL for downloading dataset contents
url = dataset.get_download_link()
print("Download URL:", url)
```

The [`get_download_link`](https://docs.ultralytics.com/hub/sdk/reference/modules/datasets/#hub_sdk.modules.datasets.Datasets.get_download_link) method documentation provides additional details.

## Upload Dataset

Uploading your dataset is straightforward. Set your dataset's ID and the file path, then use the `upload_dataset` function:

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

# Select the dataset
dataset = client.dataset("<Dataset ID>")  # Substitute with the real dataset ID

# Upload the dataset file
dataset.upload_dataset(file="<Dataset File>")  # Specify the correct file path
print("Dataset has been uploaded.")
```

The [`upload_dataset`](https://docs.ultralytics.com/hub/sdk/reference/modules/datasets/#hub_sdk.modules.datasets.Datasets.upload_dataset) method provides further details on uploading datasets. You can also learn about the related [`DatasetUpload`](https://docs.ultralytics.com/hub/sdk/reference/base/server_clients/) class.

Remember to double-check your Dataset IDs and file paths to ensure everything runs smoothly.

If you encounter any issues or have questions, our [support team](https://www.ultralytics.com/support) is here to help. 🤝

Happy data wrangling, and may your models be accurate and insightful! 🌟
