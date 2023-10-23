# Ultralytics HUB-SDK

## Where to start

- Install `hub-sdk` with pip and get up and running in minutes [Quickstart](quickstart.md)

### Installing from PyPI

To install the latest stable release of HUB-SDK from PyPI, run the following command:

```sh
pip install hub-sdk
```

## Initilize HUBClient
In the provided code snippet, you are attempting to initialize an HUBClient object, presumably for some kind of API or service access. You have two options for providing credentials: using an API key or using an email/password combination.

```sh
crednetials = {"api_key": "<ADD-API-KEY>"}
```

In this option, you are initializing the HUBClient by providing an API key in the credentials dictionary. This is commonly used when you have an API that requires an API key for authentication.

```sh
crednetials = {"email": "<EMAIL>", "password": "<PASSWORD>"}
```
In this option, you are initializing the HUBClient by providing an email and password in the credentials dictionary. This is typically used when you need to authenticate using a username (email) and password combination.


```sh
client = HUBClient(crednetials)
```

In this line of code, a client for the HUB service is being initialized with the provided credentials. The HUBClient class is used to create a connection to the HUB platform, with authentication details such as an API key or email/password pair stored in the credentials dictionary.

