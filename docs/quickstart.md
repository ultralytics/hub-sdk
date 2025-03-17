---
comments: true
description: Get started with Ultralytics HUB-SDK quickly. Follow our step-by-step guide for easy installation and initialization using Python. Perfect for all skill levels!
keywords: Ultralytics, HUB-SDK, installation, Python, setup, guide, API key, authentication, Git, PyPI
---

# Quickstart: Installing Ultralytics HUB-SDK

Welcome! 🎉 This guide provides a step-by-step walkthrough for installing and initializing the Ultralytics HUB-SDK, designed for both seasoned developers and beginners.

## Prerequisites

Ensure you have the necessary tools installed:

- **Python**: Required for working with HUB-SDK. If not already installed, download the latest version from [python.org](https://www.python.org/downloads/).
- **Git (Optional)**: Recommended for accessing the latest features directly from the source. Obtain Git from [git-scm.com](https://git-scm.com/downloads/).

## Installation

Install the HUB-SDK using one of the following methods:

### Install from PyPI

For a stable and easy installation, install the latest release of HUB-SDK from PyPI using `pip`:

```bash
pip install hub-sdk
```

This command downloads and installs the stable version of HUB-SDK into your Python environment, providing the quickest route to get started.

## Initialize HUBClient

After installation, initialize `HUBClient` to interface with the Ultralytics ecosystem. There are two authentication methods available:

### Option 1: Using an API Key

Use an API key for a simple and secure setup:

```python
credentials = {"api_key": "<YOUR-API-KEY>"}
```

Replace `<YOUR-API-KEY>` with your actual API key from Ultralytics. This method is preferred for secure API access.

### Option 2: Using Email and Password

Alternatively, use an email and password combination:

```python
credentials = {"email": "<YOUR-EMAIL>", "password": "<YOUR-PASSWORD>"}
```

Replace `<YOUR-EMAIL>` and `<YOUR-PASSWORD>` with your Ultralytics login credentials.

### Create HUBClient Object

Create a `HUBClient` object using your chosen authentication method:

!!! Example "HUB SDK Authentication"

    === "Authentication with API Key"

        ```python
        from hub_sdk import HUBClient

        credentials = {"api_key": "<YOUR-API-KEY>"}  # API key
        client = HUBClient(credentials)
        ```

    === "Authentication with Email and Password"

        ```python
        from hub_sdk import HUBClient

        credentials = {"email": "<YOUR-EMAIL>", "password": "<YOUR-PASSWORD>"}  # Email and password
        client = HUBClient(credentials)
        ```
With the `HUBClient` instance, you can perform various operations using Ultralytics services. For more details, see the [HUB-SDK](../sdk/) documentation.

---

You're all set! 🚀 With HUB-SDK installed and `HUBClient` initialized, explore the features of the Ultralytics ecosystem. For further guidance, refer to the [Ultralytics HUB-SDK documentation](https://docs.ultralytics.com/hub/sdk/) and if you encounter any issues, our support team is ready to assist. Happy coding!
