---
comments: true
description: Follow this quickstart guide to install HUB-SDK for a seamless integration with Ultralytics services.
keywords: HUB-SDK installation, HUBClient setup, Python, PyPI, Docker, API key authentication, email authentication
---

# Quickstart: Installing HUB-SDK

Hello and welcome! 🎉 If you're looking to integrate with Ultralytics services swiftly and without hassle, you've come to the right place. Our HUB-SDK installation guide is designed to help you get up and running in no time with clear, step-by-step instructions. Whether you're a seasoned developer or just starting out, our aim is to provide you with an easy, straightforward setup process. So grab your favorite beverage, and let's embark on this installation journey together!

## Prerequisites

Before we dive into the core of the installation, let's make sure we have all the tools we'll need. A smooth installation process begins with the right setup, so here's what you should have at hand:

- **Python:** It's essential to have Python installed on your machine to work with HUB-SDK. Download the latest version from [python.org](https://www.python.org/downloads/) if it isn't already set up on your system.

- **Git (Optional):** While Git isn't mandatory for installing HUB-SDK, it's strongly recommended if you want to grab the latest and greatest features straight from the source. Git can be obtained from [git-scm.com](https://git-scm.com/downloads).

With these prerequisites out of the way, you're all primed to move on to the installation phase.

## Installation Methods

Depending on your needs, you can choose between two primary methods to install the HUB-SDK. Here's what each path has to offer:

### Installing from PyPI

If you're looking for stability and ease of installation, grabbing the latest stable release of HUB-SDK from PyPI is the way to go. Here's how you can do that with pip, Python's package installer:

```sh
pip install hub-sdk
```

Running this command will pull the stable version of HUB-SDK and install it straight into your Python environment. It's the quickest route to getting started with HUB-SDK.

## Initialize HUBClient

Once the installation is complete, it's time to get your hands on the HUBClient. The HUBClient will be your gateway to interfacing with the Ultralytics ecosystem. Below you can find two ways to authenticate and use the client.

### Option A: Using an API Key for Authentication

For those who prefer using API keys for simplicity and security, here's how you set it up:

```python
credentials = {"api_key": "<YOUR-API-KEY>"}
```

Insert your actual API key provided by Ultralytics in place of `<YOUR-API-KEY>`. This is the preferred method when APIs require a secure key for access.

### Option B: Using an Email/Password Pair for Authentication

If you need to use an email/password combination, it's just as simple:

```python
credentials = {"email": "<YOUR-EMAIL>", "password": "<YOUR-PASSWORD>"}
```

Replace `<YOUR-EMAIL>` and `<YOUR-PASSWORD>` with your login credentials. This approach is more traditional but equally robust.

Finally, create the HUBClient object with your selected credential method:

```python
client = HUBClient(credentials)
```

By executing the above line of code, you've successfully created an instance of the HUBClient, ready to perform various operations using the Ultralytics services!

---

You're all set! 🚀 You now have HUB-SDK installed and an initialized HUBClient at your disposal. From here, you can start diving into the rich features provided by the Ultralytics ecosystem. Leverage the power and flexibility of HUB-SDK for your projects, navigate through the documentation to explore what more you can do, and if you encounter any issues, our friendly support team is just a click away. Happy coding!
