# Quickstart: Installing HUB-SDK

Welcome to the HUB-SDK installation guide! We'll guide you through setting up HUB-SDK, a versatile tool for various tasks. Follow these simple steps to ensure a smooth and professional installation experience. Let's get started!

## Prerequisites

Make sure you've got everything you need before starting by checking these prerequisites:

- **Python:** Make sure Python is installed on your computer. If you don't have it yet, you can download and install Python from [python.org](https://www.python.org/downloads/).

- **Git (Optional):** Before installing the HUB-SDK from GitHub, ensure that you have Git installed on your computer. If you don't have Git yet, you can easily download it from [git-scm.com](https://git-scm.com/downloads).

## Installation Methods

There are two main approaches to install the HUB-SDK: utilizing PyPI for the latest stable release or cloning the Ultralytics GitHub repository for the most current version. Furthermore, Docker offers an alternative by enabling the execution of HUB-SDK within an isolated container, eliminating the necessity for a local installation.

### Installing from PyPI

To install the most recent stable release of HUB-SDK from PyPI, execute the following command:

```sh
pip install hub-sdk
```

## Initialize HUBClient

In the given code snippet, you are endeavoring to instantiate an HUBClient object, likely for accessing an API or service. You face a choice for supplying credentials: either employ an API key or opt for an email/password combination.

```python
credentials = {"api_key": "<ADD-API-KEY>"}
```

In this alternative, you initiate the HUBClient by supplying an API key within the credentials dictionary. This is frequently employed when dealing with an API that mandates an API key for authentication.

```python
credentials = {"email": "<EMAIL>", "password": "<PASSWORD>"}
```

In this scenario, you initiate the HUBClient by supplying an email and password within the credentials dictionary. This approach is commonly employed when authentication necessitates a combination of a username (email) and password.

```python
client = HUBClient(credentials)
```

In this code line, credentials are used to set up a connection to the HUB service via the HUBClient class, initializing a client with the provided authentication details, like an API key or email/password pair stored in the credentials dictionary.
