# Ultralytics HUB-SDK

## Where to start

- Install `hub-sdk` with pip and get up and running in minutes [Quickstart](quickstart.md)

### Installing from PyPI

To install the latest stable release of HUB-SDK from PyPI, run the following command:

```sh
pip install hub-sdk
```

## Initialize HUBClient
In the given code snippet, the aim is to instantiate an HUBClient object to facilitate access to an API or service. You can choose between two credential options: utilizing an API key or opting for an email/password combination.

```python
credentials = {"api_key": "<ADD-API-KEY>"}
```

In this scenario, you're setting up the HUBClient by including an API key in the credentials dictionary. This is typically done when you're working with an API that needs an API key for authentication.

```python
credentials = {"email": "<EMAIL>", "password": "<PASSWORD>"}
```
In this scenario, you set up the HUBClient by giving your email and password in the credentials dictionary. This is commonly done when you want to log in with a username (email) and password.

```python
client = HUBClient(credentials)
```

This code initializes a client for the HUB service by using the HUBClient class. The client establishes a connection to the HUB platform and is configured with authentication details, which are stored in a dictionary. These authentication details typically include an API key or an email/password pair.
