---
comments: true
description: Learn how to manage datasets efficiently in Python using the Ultralytics HUB-SDK. Get, create, update, delete, list, and upload datasets easily.
keywords: Ultralytics, HUB-SDK, dataset management, Python, get dataset, create dataset, update dataset, delete dataset, list datasets, upload dataset, machine learning
---

# Dataset Management Operations with Ultralytics HUB-SDK

**Welcome to the Ultralytics HUB-SDK Dataset Management Documentation!** 👋

Managing datasets efficiently is crucial in the world of Machine Learning. Whether you're a seasoned data scientist or a beginner in the field, knowing how to handle dataset operations can streamline your workflow. This page covers the basics of performing operations on datasets using Ultralytics HUB-SDK in Python. The examples provided illustrate how to get, create, update, delete, list datasets, get a URL for dataset access, and upload datasets.

Let's dive in! 🚀

### Get a Dataset by ID

Looking for a specific dataset? Fetch it rapidly using its unique ID with the code snippet below. This will let you access essential information, including its data.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

# Fetch a dataset by ID
dataset = client.dataset("<Dataset ID>")  # Replace with your actual Dataset ID
print(dataset.data)  # This prints the dataset information
```

### Create a Dataset

Ready to start a new project? Follow the steps below to create a fresh dataset. All you need is to define a friendly name for your dataset and use the `create_dataset` method.

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

### Update a Dataset

As projects evolve, so should your datasets. If you need to modify your dataset's metadata, it's as simple as running the following code with the new details.

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

### Delete a Dataset

If you ever need to remove a dataset, whether to declutter your workspace or because it's no longer needed, you can permanently delete it by invoking the `delete` method as shown here.

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

### List Datasets

To browse through your datasets or find the one you need, you can list all your datasets with pagination. It is helpful when dealing with a large number of datasets.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

# Retrieve the first page of datasets
dataset = client.dataset_list(page_size=10)
print("Current dataset:", dataset.results)  # Show the datasets on the current page

# Move to the next page and show results
dataset.next()
print("Next page result:", dataset.results)

# Go back to the previous page
dataset.previous()
print("Previous page result:", dataset.results)
```

### Get URL from Storage

This convenient function fetches a URL for dataset storage access, making it a breeze to download dataset files or artifacts stored remotely.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

# Define the dataset ID for which you want a download link
dataset = client.dataset("<Dataset ID>")  # Don't forget to replace Dataset ID with the actual dataset ID

# Retrieve the URL for downloading dataset contents
url = dataset.get_download_link()
print("Download URL:", url)
```

### Upload Dataset

Uploading your dataset is a straightforward process. Set your dataset's ID and the file path you wish to upload, then utilize the `upload_dataset` function as detailed below.

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}
client = HUBClient(credentials)

# Select the dataset
dataset = client.dataset("<Dataset ID>")  # Substitute with the real dataset ID

# Upload the dataset file
dataset.upload_dataset(file="<Dataset File>")  # Make sure to specify the correct file path
print("Dataset has been uploaded.")
```

Remember, when you're working with datasets, it's always a good practice to check and verify each step of the process. Double-check your Dataset IDs and file paths to ensure everything runs smoothly.

Should you encounter any issues or have any questions, our friendly support team is here to help you navigate through any challenges. 🤝

Happy data wrangling, and may your models be accurate and insightful! 🌟
