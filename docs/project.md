---
comments: true
description: Master project management using Ultralytics HUB-SDK. Learn to create, update, delete, and list ML projects with easy Python code snippets.
keywords: Ultralytics, HUB-SDK, project management, machine learning, Python, create project, update project, delete project, list projects
---

# Project - Ultralytics HUB-SDK Operations

Welcome to the Ultralytics HUB-SDK documentation! This guide walks you through the essentials of managing your machine learning projects using the HUB-SDK. We cover everything from creating a new project and [updating existing ones](https://docs.ultralytics.com/hub/sdk/project/#update-an-existing-project) to navigating through lists of projects, all with easy-to-follow Python code snippets. Our goal is to provide a seamless and straightforward experience, allowing you to focus on building and deploying exceptional machine learning models. Let's dive in 🏊!

## Fetch a Project by ID

To retrieve a project hosted on the Ultralytics platform and view its details or make changes, fetch it by its unique ID. Pass the ID to the `client.project` function as shown in the snippet below:

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}  # Replace with your API key
client = HUBClient(credentials)

project = client.project("<Project ID>")  # Replace '<Project ID>' with your actual project ID
print(project.data)  # Displays the project's data
```

For more details, see the [reference for `hub_sdk/modules/projects.py`](https://docs.ultralytics.com/hub/sdk/reference/modules/projects/).

## Create a New Project

Begin a new machine learning project by [creating a project](https://docs.ultralytics.com/hub/projects/#create-project) in Ultralytics HUB. The following Python code outlines how to define project details (in this case, its name) and create the project using the `create_project` method:

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}  # Replace with your API key
client = HUBClient(credentials)

data = {"meta": {"name": "my project"}}  # Define the project name
project = client.project()  # Initialize a project instance
project.create_project(data)  # Create the new project with the specified data
```

## Update an Existing Project

Easily update your project's metadata by specifying the project ID and the new details. This could include a [name change](https://docs.ultralytics.com/hub/projects/#edit-project), description update, or other modifiable properties. Execute these changes with the following code snippet:

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}  # Replace with your API key
client = HUBClient(credentials)

project = client.project("<Project ID>")  # Replace with your actual project ID
project.update({"meta": {"name": "Project name update"}})  # Update the project's name or other metadata
```

## Delete a Project

To remove a project from the Ultralytics platform, use the `delete` method on the project object. The following snippet guides you through deleting a project using its ID:

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}  # Replace with your API key
client = HUBClient(credentials)

project = client.project("<Project ID>")  # Replace with the project ID to delete
project.delete()  # Permanently deletes the project
```

## List and Navigate Projects

Browse through your projects or explore [public projects](https://docs.ultralytics.com/hub/projects/#share-project) on Ultralytics by fetching a list with your desired page size. The code snippet below demonstrates how to view the current page results, navigate to the next page, and return to the previous one:

```python
from hub_sdk import HUBClient

credentials = {"api_key": "<YOUR-API-KEY>"}  # Replace with your API key
client = HUBClient(credentials)

projects = client.project_list(page_size=10)  # Fetch a list of projects with a specified page size
print("Current result:", projects.results)  # Display the projects on the current page

projects.next()  # Navigate to the next page
print("Next page result:", projects.results)  # Display the projects on the next page

projects.previous()  # Go back to the previous page
print("Previous page result:", projects.results)  # Confirm the projects on the previous page
```

Congratulations! You are now equipped to manage your machine learning projects on [Ultralytics HUB](https://www.ultralytics.com/hub) effortlessly. Experiment with these operations to enhance the organization and efficiency of your ML endeavors. For any questions or further assistance, feel free to reach out to our community. Happy coding! 🚀
