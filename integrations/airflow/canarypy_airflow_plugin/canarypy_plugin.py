import contextlib
import os

from airflow.models.mappedoperator import MappedOperator
from airflow.plugins_manager import AirflowPlugin

from canarypy.client import CanaryPyClient

TASK_ON_FAILURE_CALLBACK = "on_failure_callback"
TASK_ON_SUCCESS_CALLBACK = "on_success_callback"

canarypy_base_url = os.getenv("CANARYPY_URL")


def send_signal_to_canary(context):
    task_instance = context["ti"]

    CanaryPyClient(base_url=canarypy_base_url).send_signal_to_canary(
        task_instance.task.image.split(":")[0],
        task_instance.task.image.split(":")[1],
        task_instance.run_id,
        task_instance.task_id,
        task_instance.state,
    )


def _wrap_on_failure_callback(on_failure_callback):
    def custom_on_failure_callback(context):
        send_signal_to_canary(context)

        if on_failure_callback:
            on_failure_callback(context)

    return custom_on_failure_callback


def _wrap_on_success_callback(on_success_callback):
    def custom_on_success_callback(context):
        send_signal_to_canary(context)

        if on_success_callback:
            on_success_callback(context)

    return custom_on_success_callback


def task_policy(task) -> None:
    task.log.debug(f"Setting task policy for Dag: {task.dag_id} Task: {task.task_id}")

    if MappedOperator and isinstance(task, MappedOperator):  # type: ignore
        on_failure_callback_prop: property = getattr(
            MappedOperator, TASK_ON_FAILURE_CALLBACK
        )
        on_success_callback_prop: property = getattr(
            MappedOperator, TASK_ON_SUCCESS_CALLBACK
        )
        if not on_failure_callback_prop.fset or not on_success_callback_prop.fset:
            task.log.debug(
                "Using MappedOperator's partial_kwargs instead of callback properties"
            )
            task.partial_kwargs[TASK_ON_FAILURE_CALLBACK] = _wrap_on_failure_callback(
                task.on_failure_callback
            )
            task.partial_kwargs[TASK_ON_SUCCESS_CALLBACK] = _wrap_on_success_callback(
                task.on_success_callback
            )
            return

    task.on_failure_callback = _wrap_on_failure_callback(task.on_failure_callback)
    task.on_success_callback = _wrap_on_success_callback(task.on_success_callback)


def _wrap_task_policy(policy):
    if policy and hasattr(policy, "_task_policy_patched_by"):
        return policy

    def custom_task_policy(task):
        policy(task)
        task_policy(task)

    custom_task_policy._task_policy_patched_by = "canarypy_plugin"  # type: ignore[attr-defined]
    return custom_task_policy


def _patch_policy(settings):
    if hasattr(settings, "task_policy"):
        canarypy_task_policy = _wrap_task_policy(settings.task_policy)
        settings.task_policy = canarypy_task_policy


def _patch_canarypy_policy():

    with contextlib.suppress(ImportError):
        import airflow_local_settings

        _patch_policy(airflow_local_settings)

    from airflow.models.dagbag import settings

    _patch_policy(settings)


def get_latest_stable_version(artifact_url: str) -> str:
    """Custom Jinja template function.

    Args:
        artifact_url (str): Artifact URL.

    Returns:
        str: Processed output string.
    """
    if version := CanaryPyClient(base_url=canarypy_base_url).get_latest_stable_version(
        artifact_url
    ):
        return f"{artifact_url}:{version}"


class CanaryPyPlugin(AirflowPlugin):
    name = "canarypy_plugin"

    macros = [get_latest_stable_version]


_patch_canarypy_policy()
