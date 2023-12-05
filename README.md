# HUB-SDK by Ultralytics

## Quickstart: Installing HUB-SDK

Welcome to the HUB-SDK installation guide, where we'll walk you through the steps to set up HUB-SDK, a powerful tool for various tasks. Follow these instructions to ensure a smooth and professional installation experience.

  

## Prerequisites
Before you begin, make sure you have the following prerequisites in place:

  

-  **Python:** Ensure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/downloads/) if you don't have it already.

-  **Git (Optional):** If you plan to install HUB-SDK from the GitHub repository, make sure you have Git installed on your system. You can download Git from [git-scm.com](https://git-scm.com/downloads).  

## Installation Methods
There are two primary methods for installing HUB-SDK: using PyPI for the latest stable release or cloning the Ultralytics GitHub repository for the most up-to-date version. Additionally, Docker can be used to run HUB-SDK in an isolated container, eliminating the need for local installation.

### Installing from PyPI
To install the latest stable release of HUB-SDK from PyPI, run the following command:

```sh
pip install hub-sdk
```

## Usage


This guide provides step-by-step instructions on how to use the HUB-SDK to perform CRUD operations for Models, Datasets, and Projects.


### 1. Import HUB-SDK

```python
from hub_sdk import HUBClient
```

### 2. Use Credentials

Choose one of the following methods to set credentials for authentication:

### Using API Key

```python
credentials = {"api_key": "API-KEY"}
or
credentials = {"email": "USER-EMAIL", "password": "PASSWORD"}
```

### 3. Initialize the Client
Initialize the HUB-SDK client with the provided credentials.
```python
client = HUBClient(credentials)
```

### For Project
The code snippet for a project encapsulates a set of operations for managing a project within a given system. It includes creating a project, updating its data, and deleting the project. The project object represents the project associated with the specified "ID".
```python
project = client.project("ID")
create_project = project.create_project("<valid data>")
update_project = project.update("<update valid data>")
deleted_project = project.delete()
```
### For Model
This code snippet pertains to operations related to a model within the system. It defines actions for creating, updating, and deleting a model.
```python
model = client.model("ID")
create_model = model.create_project("<valid data>")
update_model = model.update("<update valid data>")
deleted_model = model.delete()
```


### For Dataset
This part of the code focuses on actions related to datasets within the system. It outlines functions for creating, updating, and deleting a dataset.
```python
dataset = client.dataset("ID")
create_dataset = dataset.create_project("<valid data>")
update_dataset = dataset.update("<update valid data>")
deleted_dataset = dataset.delete()
```

# License

Ultralytics offers two licensing options to cater to various use cases:

- **AGPL-3.0 License**: This [OSI-approved](https://opensource.org/licenses/) open-source license is suitable for students and enthusiasts, promoting open collaboration and knowledge sharing. Please see the [LICENSE](https://github.com/ultralytics/ultralytics/blob/main/LICENSE) file for more details.
- **Enterprise License**: Tailored for commercial use, this license allows seamless integration of Ultralytics software and AI models into commercial products and services, bypassing the open-source requirements of AGPL-3.0. If your use case involves embedding our solutions into a commercial offering, please reach out via [Ultralytics Licensing](https://ultralytics.com/license).

# Contact

For Ultralytics bug reports and feature requests, please visit [GitHub Issues](https://github.com/ultralytics/ultralytics/issues), and join our [Discord](https://ultralytics.com/discord) community for questions and discussions!

## Follow Us on Social Media

- [GitHub](https://github.com/ultralytics)
- [LinkedIn](https://www.linkedin.com/company/ultralytics/)
- [Twitter](https://twitter.com/ultralytics)
- [YouTube](https://youtube.com/ultralytics)
- [TikTok](https://www.tiktok.com/@ultralytics)
- [Instagram](https://www.instagram.com/ultralytics/)
- [Discord](https://ultralytics.com/discord)
