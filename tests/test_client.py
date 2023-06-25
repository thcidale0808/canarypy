import json
import os
from unittest.mock import Mock, patch

import pytest

from canarypy.client import CanaryPyClient


@pytest.fixture
def canary_py_client():
    with patch.dict(os.environ, {"CANARYPY_URL": "http://test-url"}):
        return CanaryPyClient()


def test_client_get_latest_stable_version(canary_py_client):
    artifact_url = "http://test-artifact"

    with patch.dict(os.environ, {"CANARYPY_URL": "http://test-url"}), patch(
        "requests.get",
        return_value=Mock(status_code=200, json=lambda: {"semver_version": "1.0.0"}),
    ) as mock_get:

        response = canary_py_client.get_latest_stable_version(artifact_url)
        mock_get.assert_called_once_with(
            url=f"http://test-url/release/{artifact_url}/latest"
        )
        assert response == f"1.0.0"


def test_client_send_signal_to_canary(canary_py_client):
    artifact_url = "http://test-artifact"
    version = "1.0.0"
    instance_id = "test-instance"
    description = "test-description"
    status = "test-status"

    with patch.dict(os.environ, {"CANARYPY_URL": "http://test-url"}), patch(
        "requests.post", return_value=Mock(status_code=200)
    ) as mock_post:
        canary_py_client.send_signal_to_canary(
            artifact_url, version, instance_id, description, status
        )
        mock_post.assert_called_once_with(
            url=f"http://test-url/signal",
            data=json.dumps(
                {
                    "artifact_url": artifact_url,
                    "semver_version": version,
                    "instance_id": instance_id,
                    "description": description,
                    "status": status,
                }
            ),
        )
