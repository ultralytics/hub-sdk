---
comments: true
description: Discover Ultralytics HUB-SDK documentation. Learn to integrate machine learning tools and services into your Python applications. Quickstart guide, installation & more!
keywords: Ultralytics HUB-SDK, machine learning, ML integration, Python SDK, AI tools, HUBClient, API, install HUB-SDK, Ultralytics services
---

# Ultralytics HUB-SDK

Welcome to the Ultralytics HUB-SDK documentation! If you're looking to integrate powerful machine learning tools and services into your Python applications, you've come to the right place. Whether you're an AI enthusiast, a seasoned machine learning practitioner, or a software developer looking to harness the capabilities of Ultralytics services, our SDK makes it easy and efficient.

Our friendly and professional documentation will guide you on a journey from installation to mastery of the HUB-SDK. Let's dive in and start leveraging the full power of the Ultralytics ecosystem in your projects!

## Where to Start

Ready to hit the ground running with the HUB-SDK? Our [quickstart guide](quickstart.md) offers a straightforward path to getting the SDK up and running in your Python environment.

-   Propel your development forward and streamline your setup by visiting the [Quickstart](quickstart.md) page.

### Installing from PyPI

Gain access to the latest stable release of HUB-SDK through [PyPI](https://pypi.org/project/hub-sdk/). Simply execute the command below in your terminal or shell to seamlessly add the SDK to your Python project:

```bash
pip install hub-sdk
```

After running this command, the SDK will be downloaded and installed, unlocking the capabilities of Ultralytics services in your application.

## Initialize HUBClient

Integration with Ultralytics services starts with the initialization of a `HUBClient` object. This pivotal step creates a bridge between your code and our APIs and requires appropriate credentials for authentication. You can opt for the standard API key method or use your email and password. Let's set it up together! 🚀

### Option 1: Using an API Key

To utilize the simplicity of an API key, prepare a dictionary with your key like so:

```python
# Replace <YOUR-API-KEY> with the actual key provided to you by Ultralytics.
credentials = {"api_key": "<YOUR-API-KEY>"}
```

Using an API key is a common authentication method suitable for programmatic access. It's perfect for scenarios where integrating a key directly into your framework is desired for swift and secure service interaction.  The `HUBClient` class [inherits authentication capabilities](https://docs.ultralytics.com/hub/sdk/reference/hub_client/) from the `Auth` class.

### Option 2: Using Email and Password

Prefer to harness your account credentials? Configure the `HUBClient` with your email and password in the credentials dictionary:

```python
# Replace <YOUR-EMAIL> with your email address and <YOUR-PASSWORD> with your password.
credentials = {"email": "<YOUR-EMAIL>", "password": "<YOUR-PASSWORD>"}
```

Employing your email and password is a convenient choice if you're looking for a traditional login experience or aiming to utilize personalized features tied to your Ultralytics account.

### Bringing it All Together

Now that your credentials are prepared, initiate your `HUBClient`:

!!! Example "HUB SDK Authentication"

    === "Authentication with API Key"

        ```python
        from hub_sdk import HUBClient

        credentials = {"api_key": "<YOUR-API-KEY>"}  # api key
        client = HUBClient(credentials)
        ```

    === "Authentication with Email and Password"

        ```python
        from hub_sdk import HUBClient

        credentials = {"email": "<YOUR-EMAIL>", "password": "<YOUR-PASSWORD>"}  # email and password
        client = HUBClient(credentials)
        ```

This crucial line of code crafts a new instance of the `HUBClient`, connecting you to the vast landscape of services offered by the Ultralytics platform. With your authentication details securely in place, you're all set to explore the functionalities at your fingertips! The `login` method [handles authentication](https://docs.ultralytics.com/hub/sdk/reference/hub_client/#login) using the provided credentials.

## HUB-SDK Functionalities

The Ultralytics HUB-SDK provides a range of functionalities to interact with your machine learning projects. Here are some key operations you can perform:

-   **Dataset Management**: Interact with datasets using the [`dataset`](https://docs.ultralytics.com/hub/sdk/reference/hub_client/#dataset) method, which returns a `Datasets` object.
-   **Dataset Listing**: Obtain a list of datasets with the [`dataset_list`](https://docs.ultralytics.com/hub/sdk/reference/hub_client/#dataset_list) method, which returns a `DatasetList` object.
-   **Project Management**: Manage your projects by [fetching](https://docs.ultralytics.com/hub/sdk/project/#fetch-a-project-by-id), [creating](https://docs.ultralytics.com/hub/sdk/project/#create-a-new-project), [updating](https://docs.ultralytics.com/hub/sdk/project/#update-existing-project), or [deleting](https://docs.ultralytics.com/hub/sdk/project/#delete-a-project) them.

---

Congratulations on setting up the Ultralytics HUB-SDK! You are now well-equipped to embark on your journey towards integrating cutting-edge machine learning services into your applications. Explore our further documentation for guidance on using specific APIs, and consult our [community forums](https://community.ultralytics.com/) if you encounter any hurdles. Happy coding, and may your projects thrive with the power of Ultralytics! 🌟
