<br>
<img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320">

# 🚀 Ultralytics HUB-SDK

[![HUB-SDK CI](https://github.com/ultralytics/hub-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/ultralytics/hub-sdk/actions/workflows/ci.yml) [![codecov](https://codecov.io/github/ultralytics/hub-sdk/graph/badge.svg?token=vCJeCYMyjH)](https://codecov.io/github/ultralytics/hub-sdk) <a href="https://ultralytics.com/discord"><img alt="Discord" src="https://img.shields.io/discord/1089800235347353640?logo=discord&logoColor=white&label=Discord&color=blue"></a>

Welcome to the Ultralytics HUB-SDK documentation! 📖 Our aim is to guide you through the installation process and help you get started with using HUB-SDK for your machine learning endeavors.

## 🛠 Quickstart: Installing HUB-SDK

Ready to dive into HUB-SDK? Follow these steps to set it up on your machine.

### Prerequisites

Ensure you have the following requirements met before proceeding:

- **Python:** HUB-SDK requires Python. Download and install Python from [python.org](https://www.python.org/downloads/) if it's not already installed on your system.

- **Git (Optional):** If you're looking to install HUB-SDK via the GitHub repository, you'll need Git. Grab Git from [git-scm.com](https://git-scm.com/downloads) if you don't have it.

### Installation Methods

Choose from the following options to install HUB-SDK:

#### Installing from PyPI

[![PyPI version](https://badge.fury.io/py/hub-sdk.svg)](https://badge.fury.io/py/hub-sdk) [![Downloads](https://static.pepy.tech/badge/hub-sdk)](https://pepy.tech/project/hub-sdk)

For the latest stable release of HUB-SDK, use PyPI by running the following command:

```sh
pip install hub-sdk
```

### 🚀 Usage

Let's begin using the HUB-SDK to perform CRUD operations for Models, Datasets, and Projects.

#### 1. Import HUB-SDK

Start by importing the `HUBClient` from the `hub_sdk` module:

```python
from hub_sdk import HUBClient
```

#### 2. Authenticate with Credentials

Set your credentials using one of the following methods:

##### Using API Key

```python
# Authenticate using an API key
credentials = {"api_key": "YOUR_API_KEY"}
```

or

##### Using Email and Password

```python
# Authenticate using your email and password
credentials = {"email": "YOUR_EMAIL", "password": "YOUR_PASSWORD"}
```

#### 3. Initialize the HUBClient

With your credentials ready, initialize the `HUBClient`:

```python
# Initialize the client with your credentials
client = HUBClient(credentials)
```

#### Operations

Below are code snippets demonstrating create, read, update, and delete (CRUD) operations for Projects, Models, and Datasets.

#### Project Operations

Managing projects is simple:

```python
# Manipulate a project with the given ID
project = client.project("PROJECT_ID")

# Create a new project with the specified data
create_project = project.create_project("PROJECT_DATA")

# Update the existing project with new data
update_project = project.update("UPDATE_DATA")

# Delete the project
deleted_project = project.delete()
```

#### Model Operations

Handle models effortlessly:

```python
# Engage with a model using the given ID
model = client.model("MODEL_ID")

# Create a new model providing the necessary data
create_model = model.create_project("MODEL_DATA")

# Update the model using provided data
update_model = model.update("UPDATE_DATA")

# Remove the model from the system
deleted_model = model.delete()
```

#### Dataset Operations

Datasets operations are straightforward:

```python
# Interact with a dataset using the specified ID
dataset = client.dataset("DATASET_ID")

# Establish a new dataset given the data
create_dataset = dataset.create_project("DATASET_DATA")

# Adjust the dataset with updated information
update_dataset = dataset.update("UPDATE_DATA")

# Erase the dataset
deleted_dataset = dataset.delete()
```

## 🚀 Ultralytics HUB

Experience seamless AI with [Ultralytics HUB](https://bit.ly/ultralytics_hub) ⭐, the all-in-one solution for data visualization, YOLOv5 and YOLOv8 🚀 model training and deployment, without any coding. Transform images into actionable insights and bring your AI visions to life with ease using our cutting-edge platform and user-friendly [Ultralytics App](https://ultralytics.com/app_install). Start your journey for **Free** now!

<a href="https://bit.ly/ultralytics_hub" target="_blank">
<img width="100%" src="https://github.com/ultralytics/assets/raw/main/im/ultralytics-hub.png" alt="Ultralytics HUB preview image"></a>

## 💡 Contribute

We're thrilled to have you contribute to Ultralytics' open-source projects! Your support and contributions make a world of difference. Get involved by checking out our [Contributing Guide](https://docs.ultralytics.com/help/contributing), and share your feedback through our [Survey](https://ultralytics.com/survey?utm_source=github&utm_medium=social&utm_campaign=Survey). A massive thank you 🙏 to everyone who contributes!

<a href="https://github.com/ultralytics/yolov5/graphs/contributors">
<img width="100%" src="https://github.com/ultralytics/assets/raw/main/im/image-contributors.png" alt="Ultralytics open-source contributors"></a>

## 📄 License

Ultralytics provides two types of licensing options:

- **AGPL-3.0 License**: An [OSI-approved](https://opensource.org/licenses/) open-source license. Ideal for academics, researchers, and enthusiasts, this license promotes sharing knowledge and collaboration. See the [LICENSE](https://github.com/ultralytics/ultralytics/blob/main/LICENSE) file for details.

- **Enterprise License**: Tailored for commercial applications, this license allows for the integration of Ultralytics software into proprietary products and services. If you're considering using our solutions commercially, please get in touch through [Ultralytics Licensing](https://ultralytics.com/license).

## 🤝 Contact

- Submit Ultralytics bug reports and feature requests via [GitHub Issues](https://github.com/ultralytics/hub-sdk/issues).
- Join our [Discord](https://ultralytics.com/discord) for assistance, questions, and discussions with the community and team!

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
