# CanaryPy - A Complete Canary Release System

## Introduction

CanaryPy is a robust, comprehensive solution to implement a canary release system for your applications. It is designed to progressively roll out changes to your software, limiting the blast radius of unforeseen issues and allowing you to quickly roll back if things go south. The system is comprised of a FastAPI application, a Streamlit application, a command-line interface (CLI), and a Python client.

## FastAPI Application

The FastAPI application serves as the backend for CanaryPy, providing RESTful APIs for managing products, releases, and signals.

### Summary

The application provides endpoints for creating and retrieving products and their respective releases. It also includes endpoints for creating and retrieving signals related to each release.

### Endpoints

- `/product`: POST endpoint to add a new product.
- `/release`: POST endpoint to add a new release of a product.
- `/release/{product_name}/latest`: GET endpoint to retrieve the latest stable release of a product.
- `/signal`: POST endpoint to add a new signal related to a release.

### How to run

1. Set the base URL as an environment variable, or pass it as an argument when initiating the FastAPI application.
2. Run the FastAPI application using Uvicorn or any ASGI server: `uvicorn main:app --reload`

## Streamlit Application

The Streamlit application serves as a web-based user interface for visualizing the release metrics.

### Summary

The application fetches the metrics data from the FastAPI backend and displays it in a user-friendly format, helping you understand the release trends and signal patterns.

### How to run

1. Set the base URL as an environment variable, or pass it as an argument when initiating the Streamlit application.
2. Run the Streamlit application: `streamlit run app.py`

## Command Line Interface (CLI)

CanaryPy also includes a CLI for users who prefer a command-line tool to interact with the system.

### Summary

The CLI provides commands to interact with products, releases, and signals.

### Commands

- `add-product`: Adds a new product.
- `add-release`: Adds a new release for a product.
- `get-latest-release`: Fetches the latest stable release for a product.
- `add-signal`: Adds a signal for a release.

### How to run

1. Set the base URL as an environment variable, or pass it as an argument when initiating the CLI application.
2. Run the respective command to interact with the system. For example, to add a product: `python cli.py add-product --product <product-details>`

## Python Client

The Python client serves as a programmatic interface to interact with the CanaryPy system, which could be used for integrating with other Python-based systems.

### Summary

The client provides methods to fetch the latest stable release and to send a signal to the Canary release system.

### Methods

- `get_latest_stable_version(product_name: str)`: Fetches the latest stable release of a product.
- `send_signal_to_canary()`: Sends a signal to the Canary release system.

### How to use

Initialize the client with the base URL of the Canary system, and call the methods as required. For example:

```python
client = CanaryPyClient(base_url="http://localhost:8000")
latest_version = client.get_latest_stable_version('product_name')
```

## Running Tests

The CanaryPy system includes a suite of tests that can be run using pytest.

To run the tests:

1. Install pytest if you haven't done so already: `pip install pytest`
2. Run pytest from the project's root directory: `pytest`

If everything is set up correctly, you should see the