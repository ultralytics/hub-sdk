# Project Management Operations

### Get Project by ID

This code snippet illustrates how to fetch a project using its unique ID. Simply provide the ID as an argument to the client. Project function, and you can access information about the project, including its data.

```python
project = client.project('<Project ID>')
print(project.data)
```

### Create Project

The code below demonstrates how to create a new project. First, import the necessary libraries, and then define the data you want to associate with the project, such as its name. Next, create the project using the _create_project_ method of the client library.

```python
data = {"meta": {"name": "my project"}}
project = client.project()
project.create_project(data)
```

### Update Project

In this code snippet, we demonstrate updating a project's metadata by specifying the project ID and providing new information, like the revised name. The update method enables the modification of project properties.

```python
project = client.project('<Project ID>')
project.update({"meta": {"name": "Project name update"}})
```

### Delete Project

This code snippet demonstrates how to delete a project. Simply specify the project's ID, and then call the delete method on the project object to remove it permanently.

```python
project = client.project("<Project ID>")
project.delete()
```

# List Projects

This code snippet retrieves a list of projects using a specified page size. It displays the current page's results, advances to the next page, and prints those results. This cycle continues until all available projects are fetched. By setting _"public=True"_ in the _project_list_ arguments, it retrieves all public projects.

```python
projects = client.project_list(page_size=10)
print("Current result:", projects.results)
projects.next()
print("Previous page result:", projects.results)
projects.previous()
print("Previous page result:", projects.results)
```
