---
comments: true
description: Learn how to install and initialize the Ultralytics HUB-SDK for streamlined API access and service interaction.
keywords: Ultralytics, HUB-SDK installation, HUBClient initialization, Python SDK, API interaction
---

# Ultralytics HUB-SDK

Welcome to the Ultralytics HUB-SDK documentation! If you're looking to integrate powerful machine learning tools and services into your Python applications, you've come to the right place. Whether you're an AI enthusiast, a seasoned machine learning practitioner, or a software developer looking to harness the capabilities of Ultralytics services, our SDK makes it easy and efficient.

Our friendly and professional documentation will guide you on a journey from installation to mastery of the HUB-SDK. Let's dive in and start leveraging the full power of the Ultralytics ecosystem in your projects!

## Where to Start

Ready to hit the ground running with the HUB-SDK? Our quickstart guide offers a straightforward path to getting the SDK up and functioning in your Python environment.

- Propel your development forward and streamline your setup by visiting: [Quickstart](quickstart.md).

### Installing from PyPI

Gain access to the latest stable release of HUB-SDK through PyPI. Simply execute the command below in your terminal/shell to seamlessly add the SDK to your Python project:

```bash
pip install hub-sdk
```

After running this command, the SDK will be downloaded and installed, unlocking the capabilities of Ultralytics services in your application.

## Initialize HUBClient

Integration with Ultralytics services starts with the initialization of an `HUBClient` object. This pivotal step creates a bridge between your code and our APIs, and it requires appropriate credentials for authentication. You can opt for the standard API key method or use your email and password. Let's set it up together! 🚀

### Option 1: Using an API Key
To utilize the simplicity of an API key, prepare a dictionary with your key like so:

```python
from hub_sdk import HUBClient

# Replace <YOUR-API-KEY> with the actual key provided to you by Ultralytics.
credentials = {"api_key": "<YOUR-API-KEY>"}
```

By using an API key, you're choosing a common authentication method suitable for programmatic access. It's perfect for scenarios where integrating a key directly into your framework is desired for swift and secure service interaction.

### Option 2: Using Email and Password
Prefer to harness your account credentials? Configure the `HUBClient` with your email and password in the credentials dictionary:

```python
from hub_sdk import HUBClient

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

This crucial line of code crafts a new instance of the HUBClient, connecting you to the vast landscape of services offered by the Ultralytics platform. With your authentication details securely in place, you're all set to explore the functionalities at your fingertips!

---

Congratulations on setting up the Ultralytics HUB-SDK! You are now well-equipped to embark on your journey towards integrating cutting-edge machine learning services into your applications. Explore our further documentation for guidance on using specific APIs, and consult our community forums if you encounter any hurdles. Happy coding, and may your projects thrive with the power of Ultralytics! 🌟
