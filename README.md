<a href="https://www.ultralytics.com/"><img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320" alt="Ultralytics logo"></a>

# Ultralytics HUB-SDK

[![HUB-SDK CI](https://github.com/ultralytics/hub-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/ultralytics/hub-sdk/actions/workflows/ci.yml)
[![Ultralytics Discord](https://img.shields.io/discord/1089800235347353640?logo=discord&logoColor=white&label=Discord&color=blue)](https://discord.com/invite/ultralytics)
[![Ultralytics Forums](https://img.shields.io/discourse/users?server=https%3A%2F%2Fcommunity.ultralytics.com&logo=discourse&label=Forums&color=blue)](https://community.ultralytics.com/)
[![Ultralytics Reddit](https://img.shields.io/reddit/subreddit-subscribers/ultralytics?style=flat&logo=reddit&logoColor=white&label=Reddit&color=blue)](https://reddit.com/r/ultralytics)

Welcome to the Ultralytics HUB-SDK documentation! 📖 This guide will walk you through the installation process and help you get started using the HUB-SDK for your [machine learning (ML)](https://www.ultralytics.com/glossary/machine-learning-ml) projects. The SDK provides tools to interact programmatically with [Ultralytics HUB](https://platform.ultralytics.com/).

## 🚀 Quickstart: Installing HUB-SDK

Ready to dive into the HUB-SDK? Follow these steps to set it up on your machine.

### Prerequisites

Before you begin, ensure your system meets the following requirements:

- **Python:** The HUB-SDK requires Python 3.8 or later. If you don't have Python installed, download it from the official [Python website](https://www.python.org/downloads/).
- **Git (Optional):** If you plan to install the HUB-SDK directly from the GitHub repository or contribute to the project, you'll need Git. Install Git from [git-scm.com](https://git-scm.com/downloads/) if necessary.

### Installation Methods

You can install the HUB-SDK using either of the following methods:

#### Install from PyPI

For the latest stable release, install the HUB-SDK from [PyPI](https://pypi.org/project/hub-sdk/) using pip:

[![PyPI - Version](https://img.shields.io/pypi/v/hub-sdk?logo=pypi&logoColor=white)](https://pypi.org/project/hub-sdk/) [![Ultralytics Downloads](https://static.pepy.tech/badge/hub-sdk)](https://clickpy.clickhouse.com/dashboard/hub-sdk) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hub-sdk?logo=python&logoColor=gold)](https://pypi.org/project/hub-sdk/)

```sh
pip install hub-sdk
```

#### Install from GitHub

To get the very latest development version, you can clone the repository and install it locally:

```sh
git clone https://github.com/ultralytics/hub-sdk.git
cd hub-sdk
pip install -e .
```

## 🛠️ Usage

Let's get started using the HUB-SDK to perform Create, Read, Update, and Delete ([CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)) operations for Models, Datasets, and Projects on Ultralytics HUB.

### 1. Authenticate with Credentials

You need to authenticate your client. Choose one of the following methods:

#### Using an API Key

You can find or generate your API key in your Ultralytics HUB account settings.

```python
# Authenticate using your API key
credentials = {"api_key": "YOUR_API_KEY"}
```

#### Using Email and Password

Alternatively, authenticate using your Ultralytics HUB email and password.

```python
# Authenticate using your email and password
credentials = {"email": "YOUR_EMAIL", "password": "YOUR_PASSWORD"}
```

### 2. Initialize the HUBClient

Instantiate the `HUBClient` with your chosen credentials:

```python
# Initialize the client with your credentials
from hub_sdk import HUBClient

client = HUBClient(credentials)
```

### Operations

The following code snippets demonstrate how to perform CRUD operations on Projects, Models, and Datasets using the initialized client.

#### Project Operations

Manage your projects easily:

```python
# Get a specific project by its ID
project = client.project("PROJECT_ID")

# Create a new project
project = client.project()
project.create_project({"meta": {"name": "My Project"}})

# List projects
projects = client.project_list(page_size=10)

# Update an existing project
project = client.project("PROJECT_ID")
project.update({"meta": {"name": "Updated Project"}})

# Delete the project
project.delete()
```

#### Model Operations

Handle your models efficiently:

```python
# Get a specific model by its ID
model = client.model("MODEL_ID")

# Create a new model
model = client.model()
model.create_model(
    {
        "meta": {"name": "My Model"},
        "projectId": "PROJECT_ID",
        "datasetId": "DATASET_ID",
        "config": {
            "batchSize": -1,
            "cache": "ram",
            "device": "cpu",
            "epochs": 5,
            "imageSize": 640,
            "patience": 5,
        },
    }
)

# List models associated with a project or account
models = client.model_list(page_size=10)

# Update model details
model = client.model("MODEL_ID")
model.update({"meta": {"name": "Updated Model"}})

# Upload a model checkpoint
model.upload_model(epoch=5, weights="path/to/best.pt", is_best=True)

# Delete the model
model.delete()
```

#### Dataset Operations

Dataset management is straightforward:

```python
# Get a specific dataset by its ID
dataset = client.dataset("DATASET_ID")

# Create a new dataset
dataset = client.dataset()
dataset.create_dataset({"meta": {"name": "My Dataset"}, "filename": "dataset.zip"})

# List datasets
datasets = client.dataset_list(page_size=10)

# Update dataset details
dataset = client.dataset("DATASET_ID")
dataset.update({"meta": {"name": "Updated Dataset"}})

# Upload dataset contents
dataset.upload_dataset(file="path/to/dataset.zip")

# Delete the dataset
dataset.delete()
```

For additional payload fields, pagination helpers, and response details, see the [HUB-SDK documentation](https://docs.ultralytics.com/platform) and the [source classes](https://github.com/ultralytics/hub-sdk/tree/main/hub_sdk/modules/).

## ⭐ Ultralytics HUB

Experience seamless AI development with [Ultralytics HUB](https://platform.ultralytics.com/) ⭐, the ultimate platform for building, training, and deploying computer vision models. Visualize your [datasets](https://docs.ultralytics.com/datasets), train [Ultralytics YOLO](https://docs.ultralytics.com/models/yolo11) models like YOLO11 🚀, and deploy them to real-world applications without writing any code. Explore our user-friendly [Ultralytics App](https://www.ultralytics.com/app-install) and leverage cutting-edge tools to bring your AI visions to life. Start your journey for **Free** today!

<a href="https://platform.ultralytics.com/" target="_blank">
<img width="100%" src="https://github.com/ultralytics/assets/raw/main/im/ultralytics-hub.png" alt="Ultralytics HUB preview image"></a>

## 💡 Contribute

We welcome contributions to our open-source projects! Your support helps us improve and grow. To get involved, please see our [Contributing Guide](https://docs.ultralytics.com/help/contributing). We also appreciate feedback – let us know your thoughts via our [Survey](https://www.ultralytics.com/survey?utm_source=github&utm_medium=social&utm_campaign=Survey). Thank you 🙏 to all our contributors!

[![Ultralytics open-source contributors](https://raw.githubusercontent.com/ultralytics/assets/main/im/image-contributors.png)](https://github.com/ultralytics/ultralytics/graphs/contributors)

## 📄 License

Ultralytics offers two licensing options to accommodate different use cases:

- **AGPL-3.0 License**: This [OSI-approved](https://opensource.org/license/agpl-3.0) open-source license is ideal for students, researchers, and enthusiasts who wish to share their work and collaborate openly. See the [LICENSE](https://github.com/ultralytics/hub-sdk/blob/main/LICENSE) file for full details.
- **Enterprise License**: Designed for commercial use, this license allows for the integration of Ultralytics software and AI models into commercial products and services without the open-source requirements of AGPL-3.0. If your scenario involves commercial deployment, please contact us via [Ultralytics Licensing](https://www.ultralytics.com/license).

## 🤝 Contact

For bug reports and feature requests related to the HUB-SDK, please use [GitHub Issues](https://github.com/ultralytics/hub-sdk/issues). For questions, support, and discussions with the Ultralytics team and the wider community, join our [Discord](https://discord.com/invite/ultralytics)!

<br>
<div align="center">
  <a href="https://github.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-github.png" width="3%" alt="Ultralytics GitHub"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.linkedin.com/company/ultralytics/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-linkedin.png" width="3%" alt="Ultralytics LinkedIn"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://twitter.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-twitter.png" width="3%" alt="Ultralytics Twitter"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://youtube.com/ultralytics?sub_confirmation=1"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-youtube.png" width="3%" alt="Ultralytics YouTube"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.tiktok.com/@ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-tiktok.png" width="3%" alt="Ultralytics TikTok"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://ultralytics.com/bilibili"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-bilibili.png" width="3%" alt="Ultralytics BiliBili"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://discord.com/invite/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-discord.png" width="3%" alt="Ultralytics Discord"></a>
</div>
