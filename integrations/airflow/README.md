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

The plugin patches the `task_policy` function in Airflow's settings. If an existing `task_policy` function exists, it is wrapped, so that the original policy is applied first, followed by the policy provided by this plugin.

The plugin's policy adds custom `on_failure_callback` and `on_success_callback` functions to the tasks. These functions send a signal to CanaryPy, containing information about the task's image, run ID, task ID, and state.

If a task is a `MappedOperator`, the policy applies the custom callbacks via the `partial_kwargs` attribute, to work around the fact that these operators do not have `on_failure_callback` and `on_success_callback` properties.

Finally, the plugin adds a `get_latest_stable_version` function to the Jinja environment, which can be used in your DAGs. This function retrieves the latest stable version of an artifact from CanaryPy, given the artifact's URL.

## Usage

With this plugin installed, your tasks in Airflow will automatically send signals to CanaryPy when they start, succeed or fail. This happens without needing any changes to your DAGs.

To use the `get_latest_stable_version` function in a Jinja template, use the following syntax:

```
{{ get_latest_stable_version('artifact_url') }}
```

## Contributing

We welcome contributions! Please feel free to submit a Pull Request.