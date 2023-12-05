<br>
<img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320">

# Ultralytics HUB-SDK

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
pip  install  hub-sdk
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
```
client = HUBClient(credentials)

```

### For Project
The code snippet for a project encapsulates a set of operations for managing a project within a given system. It includes creating a project, updating its data, and deleting the project. The project object represents the project associated with the specified "ID".
```
project = client.project("ID")
create_project = project.create_project("<valid data>")
update_project = project.update("<update valid data>")
deleted_project = project.delete()
```
### For Model
This code snippet pertains to operations related to a model within the system. It defines actions for creating, updating, and deleting a model.
```
model = client.model("ID")
create_model = model.create_project("<valid data>")
update_model = model.update("<update valid data>")
deleted_model = model.delete()
```


### For Dataset
This part of the code focuses on actions related to datasets within the system. It outlines functions for creating, updating, and deleting a dataset.
```
dataset = client.dataset("ID")
create_dataset = dataset.create_project("<valid data>")
update_dataset = dataset.update("<update valid data>")
deleted_dataset = dataset.delete()
```

# Contribute

We love your input! Ultralytics open-source efforts would not be possible without help from our community. Please see our [Contributing Guide](https://docs.ultralytics.com/help/contributing) to get started, and fill out our [Survey](https://ultralytics.com/survey?utm_source=github&utm_medium=social&utm_campaign=Survey) to send us feedback on your experience. Thank you 🙏 to all our contributors!

<!-- SVG image from https://opencollective.com/ultralytics/contributors.svg?width=990 -->
<a href="https://github.com/ultralytics/yolov5/graphs/contributors">
<img width="100%" src="https://github.com/ultralytics/assets/raw/main/im/image-contributors.png" alt="Ultralytics open-source contributors"></a>

# License

Ultralytics offers two licensing options to accommodate diverse use cases:

- **AGPL-3.0 License**: This [OSI-approved](https://opensource.org/licenses/) open-source license is ideal for students and enthusiasts, promoting open collaboration and knowledge sharing. See the [LICENSE](https://github.com/ultralytics/ultralytics/blob/main/LICENSE) file for more details.
- **Enterprise License**: Designed for commercial use, this license permits seamless integration of Ultralytics software and AI models into commercial goods and services, bypassing the open-source requirements of AGPL-3.0. If your scenario involves embedding our solutions into a commercial offering, reach out through [Ultralytics Licensing](https://ultralytics.com/license).

# Contact

For Ultralytics bug reports and feature requests please visit [GitHub Issues](https://github.com/ultralytics/hub-sdk/issues), and join our [Discord](https://ultralytics.com/discord) community for questions and discussions!

<br>
<div align="center">
  <a href="https://github.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-github.png" width="3%" alt="Ultralytics GitHub"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.linkedin.com/company/ultralytics/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-linkedin.png" width="3%" alt="Ultralytics LinkedIn"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://twitter.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-twitter.png" width="3%" alt="Ultralytics Twitter"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://youtube.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-youtube.png" width="3%" alt="Ultralytics YouTube"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.tiktok.com/@ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-tiktok.png" width="3%" alt="Ultralytics TikTok"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.instagram.com/ultralytics/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-instagram.png" width="3%" alt="Ultralytics Instagram"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://ultralytics.com/discord"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-discord.png" width="3%" alt="Ultralytics Discord"></a>
</div>
