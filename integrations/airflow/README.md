# CanaryPy Airflow Plugin

This is a plugin for Apache Airflow that provides integration with CanaryPy. It modifies the task policies in Airflow, to send signals to CanaryPy on task success or failure. It also adds a custom Jinja template function that can be used to get the latest stable version of an artifact.

## Requirements

- Python 3.8+
- Apache Airflow 2.0+
- [CanaryPy](https://pypi.org/project/canarypy/) Library

## Installation

This plugin is available in Pypi so you can add to your Airflow installation by running the following command:

```
pip install canarypy_airflow_plugin
```

Alternatively, you can add the plugin to Airflow dependencies file.

Also disable lazy loading of plugins by setting `lazy_load_plugins` to `False` in your Airflow configuration file:

```ini
[core]
lazy_load_plugins = False
```

## Configuration

The plugin uses the environment variable `CANARYPY_URL` to set the base URL for CanaryPy. This environment variable must be set before the plugin is loaded by Airflow.

## How It Works

This plugin add two main features to your Airflow instance:

* Append a function to your `on_failure_callback` and `on_success_callback` at the task level. This function is responsible to send signals to the `CanaryPy` backend.
* Adds a `get_latest_stable_version` function to the Jinja environment. This function was added as a jinja template to be executed only as runtime.

## Usage

With this plugin installed, your tasks in Airflow will automatically send signals to CanaryPy when they start, succeed or fail. This happens without needing any changes to your DAGs.

To use the `get_latest_stable_version` function in a Jinja template, use the following syntax:

```
{{ get_latest_stable_version('artifact_url') }}
```

## Contributing

We welcome contributions! Please feel free to submit a Pull Request.