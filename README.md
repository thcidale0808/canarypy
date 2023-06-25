# CanaryPy - A Complete Canary Release System

## Introduction

CanaryPy is a robust, comprehensive solution to implement a canary release system for your applications. It is designed to progressively roll out changes to your software, limiting the blast radius of unforeseen issues and allowing you to quickly roll back if things go south. The system is comprised of a FastAPI application, a Streamlit application, a command-line interface (CLI), and a Python client.

## FastAPI Application

The FastAPI application serves as the backend for CanaryPy, providing RESTful APIs for managing products, releases, and signals.

### Summary

The application provides endpoints for creating and retrieving products and their respective releases. It also includes endpoints for creating and retrieving signals related to each release.

The FastAPI application uses a PostgreSQL database to store the data. 

### Endpoints

The CanaryPy provides endpoints to manage products, releases, and signals. More details about the endpoints can be found in the `/docs` endpoint.

### How to run

1. The following environment variable can be set to start the FastAPI server:
   * `CANARYPY_API_PORT`: The base URL of the FastAPI application. Defaults to `8080`.
   * `CANARYPY_API_HOST`: The base URL of the FastAPI application. Defaults to `0.0.0.0`.
   * `CANARYPY_API_RELOAD`: Whether to reload the server when code changes are detected. Defaults to `True`.
   * `CANARYPY_API_DEBUG`: Whether to run the server in debug mode. Defaults to `True`.
   * `CANARYPY_API_LOG_LEVEL`: The log level for the server. Defaults to `info`.
   * `CANARYPY_DB_CONN_STRING`: The connection string for the database. Alternatively, you can set the connection details in separated environment variables:
     * `CANARYPY_DB_USER`: The username for the database.
     * `CANARYPY_DB_PASSWORD`: The password for the database.
     * `CANARYPY_DB_HOST`: The host for the database.
     * `CANARYPY_DB_PORT`: The port for the database.
     * `CANARYPY_DB_NAME`: The name of the database.
2. Run the FastAPI application using the following command `canarypy api start`

## Streamlit Application

The Streamlit application serves as a web-based user interface for visualizing the release metrics.

### Summary

The application fetches the metrics data from the FastAPI backend and displays it in a user-friendly format, helping you understand the release trends and signal patterns.

The Streamlit application uses a PostgreSQL database to fetch the data for the dashboard. 

### How to run

1. The following environment variable can be set to start the FastAPI server:
   * `CANARYPY_DB_CONN_STRING`: The connection string for the database. Alternatively, you can set the connection details in separated environment variables:
     * `CANARYPY_DB_USER`: The username for the database.
     * `CANARYPY_DB_PASSWORD`: The password for the database.
     * `CANARYPY_DB_HOST`: The host for the database.
     * `CANARYPY_DB_PORT`: The port for the database.
     * `CANARYPY_DB_NAME`: The name of the database.
2. Run the Streamlit application: `canarypy web start`

## How it works

CanaryPy also includes a CLI to manage the products, releases, and signals. The CLI is built using the Click library.

The CLI uses the FastAPI application as the backend and therefore the following environment variables need to be set to run the CLI:

* `CANARYPY_URL`: The base URL of the FastAPI application. Defaults to `http://localhost:8080`.

### Features available

#### Products
Products are the fist step in the CanaryPy system. A product is a software application that is being released using the CanaryPy system. The CLI provides the following commands to manage products:

`canapyry product create`

This will prompt the user to enter the details of the product, and will create the product in the system.

#### Releases
Releases are the second step in the CanaryPy system. A release is a version of a product that is being released using the CanaryPy system. The CLI provides the following commands to manage releases:

`canarypy release create --semver-version <semver> --artifact-url <product>`

This will create a new release for a product. The semver version and the artifact URL are required parameters.

it's possible to fetch the latest stable release of a product using the python client as shown below:

```python
from canarypy.client import CanaryPyClient
client = CanaryPyClient(base_url="http://localhost:8000")
client.get_latest_stable_version(product_name)
```

#### Signals
Signals are the third step in the CanaryPy system. A signal is the result of an execution of a product with a release. The CLI provides the following commands to manage signals:

`canarypy signal create --status <status> --description <description> --instance-id <instance-id>` -- semver-version <version> --artifact-url <artifact-url>`

It's also possible to send signals to the CanaryPy system using the Python client as shown below:

```python
from canarypy.client import CanaryPyClient
client = CanaryPyClient(base_url="http://localhost:8000")
client.send_signal_to_canary(artifact_url, version, instance_id, description, status)
```
