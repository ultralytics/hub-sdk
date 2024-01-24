---
comments: true
description: Access and manage your machine learning projects on Ultralytics HUB-SDK with our guided documentation.
keywords: Ultralytics HUB-SDK, project management, ML project operations, Python code examples, create project, update project, delete project
---

# Ultralytics HUB-SDK Project Management Operations

Welcome to the Ultralytics HUB-SDK documentation! Here we'll guide you through the essentials of managing your machine learning projects using the HUB-SDK. From creating a new project, updating existing one, to navigating through lists of projects, we have covered it all for you with easy-to-follow Python code snippets. Our goal is to make your experience seamless and straightforward, so you can focus on the important stuff – building and deploying exceptional machine learning models. Let's dive in 🏊!

## Fetch a Project by ID

When you already have a project hosted on the Ultralytics platform, you may want to retrieve it to see its details or make changes. To fetch a project by its unique ID, you only need to pass the ID to the `client.project` function. Below is a snippet that enables you to do just that, providing a quick peek at the project's data:

```python
project = client.project('<Project ID>')  # Replace '<Project ID>' with your actual project ID
print(project.data)
```

## Create a New Project

Are you starting a fresh ML project? Fantastic! The following Python code outlines the steps to create a new project on Ultralytics. We will import the necessary libraries, define the project details (in this case its name), and finally create the project using the `create_project` method of our HUB-SDK client library. Here's how:

```python
data = {"meta": {"name": "my project"}}  # Name your project
project = client.project()  # Initialize a project instance
project.create_project(data)  # Create your new project with the specified data
```

## Update Existing Project

Update your project's metadata with ease by specifying the project ID and the new details you want to include. This could be a name change, description update, or any other modifiable property. Find out how to execute these changes with this straightforward code snippet:

```python
project = client.project('<Project ID>')  # Provide your actual project ID here
project.update({"meta": {"name": "Project name update"}})  # Update the project's name or other metadata
```

## Delete a Project

If you no longer require a project and wish to delete it from the Ultralytics platform, you can do so with a simple call to the `delete` method on the project object. The following snippet will guide you through deleting a project using its ID:

```python
project = client.project("<Project ID>")  # Input the project ID for the project to delete
project.delete()  # This will permanently delete your project
```

## List and Navigate Projects

In some cases, you may want to browse through your projects or even check out public projects on Ultralytics. This can be done by fetching a list of projects with your desired page size. Our code snippet demonstrates how to view the current page results, navigate to the next page, and then go back to the previous one. It's a great way to explore the breadth of projects available:

```python
projects = client.project_list(page_size=10)  # Fetch a list of projects with specified page size
print("Current result:", projects.results)  # Display the projects in the current page

projects.next()  # Navigate to the next page
print("Next page result:", projects.results)  # Display the projects after pagination

projects.previous()  # Go back to the previous page
print("Previous page result:", projects.results)  # Confirm the projects in the previous page
```

Congratulations! You're now equipped with the knowledge to effortlessly manage your machine learning projects on Ultralytics HUB-SDK. Experiment with these operations, and watch as your ML endeavors become more organized and efficient. If you have any questions or need further assistance, don't hesitate to reach out to our supportive community. Happy coding! 🚀
