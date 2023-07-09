from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    "owner": "airflow",
    "description": "Use of the DockerOperator",
    "depend_on_past": False,
    "start_date": datetime(2021, 5, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "docker_operator_demo",
    default_args=default_args,
    schedule_interval="5 * * * *",
    catchup=False,
) as dag:
    t1 = DockerOperator(
        task_id="docker_command_starting",
        image='{{ macros.canarypy_plugin.get_latest_stable_version("python") }}',
        container_name="task___command_sleep",
        api_version="auto",
        auto_remove=True,
        command="echo starting",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
    )

    t2 = DockerOperator(
        task_id="docker_command_hello",
        image='{{ macros.canarypy_plugin.get_latest_stable_version("python") }}',
        container_name="task___command_sleep",
        api_version="auto",
        auto_remove=True,
        command="echo hello",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
    )

    t3 = DockerOperator(
        task_id="docker_command_world",
        image='{{ macros.canarypy_plugin.get_latest_stable_version("python") }}',
        container_name="task___command_sleep",
        api_version="auto",
        auto_remove=True,
        command="echo world",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
    )

    t1 >> t2 >> t3
