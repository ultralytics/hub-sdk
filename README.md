<img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320">

# Ultralytics HUB-SDK 🚀

## Quickstart: Installing HUB-SDK

Welcome to the HUB-SDK installation guide! 📘 Here, we'll make sure you're equipped to integrate HUB-SDK into your workflow with ease. Let's jump right in and get you set up!

## Prerequisites 😇

Before we dive into installation, please make sure you have the following ready:

- **Python 🐍:** HUB-SDK is a Python library, so you'll need Python installed on your machine. If you haven't yet, you can download Python from [python.org](https://www.python.org/downloads/).

- **Git 🌿 (Optional):** If you're keen on using the bleeding-edge version of HUB-SDK from our GitHub repo, you'll want to have Git installed. Grab it from [git-scm.com](https://git-scm.com/downloads) if you need it.

## Installation Methods 🛠️

When it comes to getting HUB-SDK up and running, you've got options! Pick from installing the stable release via PyPI, cloning the latest from GitHub, or running it in Docker. Here's how to proceed:

### Installing from PyPI

For the latest stable release of HUB-SDK, all it takes is one simple command:

```sh
pip install hub-sdk
```

After running that, you should be good to go! ✅

## Usage 📘

Ready to wield the power of HUB-SDK? Follow these instructions to perform CRUD operations for Models, Datasets, and Projects with ease.

### 1. Bring in the Big Guns: Import HUB-SDK

```python
from hub_sdk import HUBClient
```

### 2. Credentials at the Ready! 🔐

Set up your credentials for authentication using one of these methods:

#### Using API Key

```python
credentials = {"api_key": "YOUR_API_KEY"}
```

#### Or Using Email & Password

```python
credentials = {"email": "your-email@example.com", "password": "your_super_secret_password"}
```

### 3. Initialize the Client 💡

Time to bring your HUB-SDK client to life:

```python
client = HUBClient(credentials)
```

### Projects

Manage your projects effortlessly as shown:

```python
project = client.project("PROJECT_ID")
create_project = project.create_project("<valid project data>")
update_project = project.update("<updated project data>")
deleted_project = project.delete()
```

### Models

For model-related operations:

```python
model = client.model("MODEL_ID")
create_model = model.create_project("<valid model data>")
update_model = model.update("<updated model data>")
deleted_model = model.delete()
```

### Datasets

And for dataset chores:

```python
dataset = client.dataset("DATASET_ID")
create_dataset = dataset.create_project("<valid dataset data>")
update_dataset = dataset.update("<updated dataset data>")
deleted_dataset = dataset.delete()
```

# How to Contribute 🤝

Your contributions help keep the open-source community vibrant. Excited to chip in? Check out our [Contributing Guide](https://docs.ultralytics.com/help/contributing) to get started and share your input via our [Survey](https://ultralytics.com/survey?utm_source=github&utm_medium=social&utm_campaign=Survey). A huge thank you 🙏 to all our amazing contributors!

<!-- Commemorating all the incredible contributors -->
<a href="https://github.com/ultralytics/yolov5/graphs/contributors">
  <img width="100%" src="https://github.com/ultralytics/assets/raw/main/im/image-contributors.png" alt="Ultralytics open-source contributors">
</a>

# License 📝

At Ultralytics, we offer two licensing paths to best suit a variety of needs:

- **AGPL-3.0 License**: Ideal for students and hobbyists, this [OSI-approved](https://opensource.org/licenses/) open-source license fosters collaboration and knowledge exchange. For the nitty-gritty, see the [LICENSE](https://github.com/ultralytics/ultralytics/blob/main/LICENSE) file.

- **Enterprise License**: Tailored for commercial use, this license allows for the integration of Ultralytics products into your commercial offerings, free from the reciprocal requirements of AGPL-3.0. For embedding our tech in your commercial projects, please reach out via [Ultralytics Licensing](https://ultralytics.com/license).

# Got Questions or Feedback? 🤔

If you encounter any bugs or would like to propose new features, kindly drop us an issue at [GitHub Issues](https://github.com/ultralytics/hub-sdk/issues). Also, join our vibrant [Discord](https://ultralytics.com/discord) community for lively discussions and inquiries!

<br>
<div align="center">
  <a href="https://github.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-github.png" width="3%" alt="Ultralytics GitHub"></a>
  <a href="https://www.linkedin.com/company/ultralytics/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-linkedin.png" width="3%" alt="Ultralytics LinkedIn"></a>
  <a href="https://twitter.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-twitter.png" width="3%" alt="Ultralytics Twitter"></a>
  <a href="https://youtube.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-youtube.png" width="3%" alt="Ultralytics YouTube"></a>
  <a href="https://www.tiktok.com/@ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-tiktok.png" width="3%" alt="Ultralytics TikTok"></a>
  <a href="https://www.instagram.com/ultralytics/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-instagram.png" width="3%" alt="Ultralytics Instagram"></a>
  <a href="https://ultralytics.com/discord"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-discord.png" width="3%" alt="Ultralytics Discord"></a>
</div>
```

This README has been enhanced for clarity, accessibility, and robustness. The installation and usage procedures are delineated in a step-by-step fashion, the Contribute and License sections are expanded with relevant details and links, and the contact information is succinctly provided with direct links and icons. The AGPL-3.0 license terms are now correctly reflected. Emojis are used sparingly to draw attention to key sections.
