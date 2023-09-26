# Dataset Management Operations

### Get a Dataset by ID
This code snippet illustrates how to fetch a dataset using its unique ID. Simply provide the ID as an argument to the client.dataset function, and you can access information about the dataset, including its data.

```sh
dataset = client.dataset('Dataset ID')
print(dataset.data)
```

### Create a Dataset
The code above demonstrates how to create a new dataset. First, import the necessary libraries, and then define the data you want to associate with the dataset, such as its name. Next, create the dataset using the create_dataset method of the client library.
```sh
data = {"meta": {"name": "my dataset"}, "filename": ""}
dataset = client.dataset()
dataset.create_dataset(data)
```

### Update a Dataset
In this code example, we show how to update the metadata of a dataset. You need to specify the dataset's ID and provide the new metadata, such as the updated name. The update method allows you to modify dataset properties.
```sh
dataset = client.dataset("Dataset ID")
print(dataset.update({"meta": {"name": "dataset Name"}}))
```

### delete a Dataset
This code snippet demonstrates how to delete a dataset. Simply specify the dataset's ID, and then call the delete method on the dataset object to remove it permanently from your system.
```sh
dataset = client.dataset('Dataset ID')
print(dataset.data)
```

### List Datasets
Here, we showcase how to retrieve a list of datasets. You can set the desired page size to control the number of results per page. The code demonstrates how to retrieve the first page of datasets, navigate to the next page, and return to the previous page if available.

```sh
dataset = client.dataset_list(page_size=1)
print(dataset.results)
print("Next: ", dataset.results)
dataset.next()
print("Next: ", dataset.results)
dataset.previous()
print("Previous: ", dataset.results)
```