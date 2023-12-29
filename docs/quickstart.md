# Quickstart: Installing HUB-SDK

Welcome to the HUB-SDK installation guide, where we'll walk you through the steps to set up HUB-SDK, a powerful tool for various tasks. Follow these instructions to ensure a smooth and professional installation experience.

## Prerequisites

Before you begin, make sure you have the following prerequisites in place:

- **Python:** Ensure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/downloads/) if you don't have it already.

- **Git (Optional):** If you plan to install HUB-SDK from the GitHub repository, make sure you have Git installed on your system. You can download Git from [git-scm.com](https://git-scm.com/downloads).

## Installation Methods

There are two primary methods for installing HUB-SDK: using PyPI for the latest stable release or cloning the Ultralytics GitHub repository for the most up-to-date version. Additionally, Docker can be used to run HUB-SDK in an isolated container, eliminating the need for local installation.

### Installing from PyPI

To install the latest stable release of HUB-SDK from PyPI, run the following command:

```sh
pip install hub-sdk
```


## Initialize HUBClient

In the provided code snippet, you are attempting to initialize an HUBClient object, presumably for some kind of API or service access. You have two options for providing credentials: using an API key or using an email/password combination.

```sh
credentials = {"api_key": "<ADD-API-KEY>"}
```

In this option, you are initializing the HUBClient by providing an API key in the credentials dictionary. This is commonly used when you have an API that requires an API key for authentication.

```sh
credentials = {"email": "<EMAIL>", "password": "<PASSWORD>"}
```
In this option, you are initializing the HUBClient by providing an email and password in the credentials dictionary. This is typically used when you need to authenticate using a username (email) and password combination.


```sh
client = HUBClient(credentials)
```

In this line of code, a client for the HUB service is being initialized with the provided credentials. The HUBClient class is used to create a connection to the HUB platform, with authentication details such as an API key or email/password pair stored in the credentials dictionary.
