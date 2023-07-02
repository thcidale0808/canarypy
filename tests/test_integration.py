import os
from unittest.mock import Mock, patch

from canarypy.api.models.product import Product
from canarypy.api.models.release import Release
from canarypy.api.models.signal import Signal
from canarypy.cli.main import product, release, signal
from canarypy.client import CanaryPyClient


def test_integration_send_signal_to_canary(monkeypatch, client, runner, db_session):
    monkeypatch.setattr("requests.get", client.get)
    monkeypatch.setattr("requests.post", client.post)
    canarypy_base_url = client.base_url
    first_version = "1.0.0"
    instance_id = "test-instance"
    description = "test-description"
    product_name = "awsome product"
    artifact_url = "http://awesome-product.com/releases/v1.0.0"
    with patch(
        "canarypy.cli.main.prompt",
        return_value={
            "name": product_name,
            "repository_url": "http://awesome-product.com",
            "artifact_url": artifact_url,
        },
    ) as mock_prompt:
        os.environ["CANARYPY_URL"] = canarypy_base_url
        result = runner.invoke(
            product,
            ["create"],
            input="My Product\nhttps://github.com/my-product\nhttps://github.com/my-product/releases/v1.0.0\n",
        )
    assert result.exit_code == 0

    product_model = db_session.query(Product).filter(Product.name == product_name).one()

    assert product_model

    result = runner.invoke(
        release,
        ["create", "--artifact-url", artifact_url, "--semver-version", first_version],
    )

    assert result.exit_code == 0

    release_model = (
        db_session.query(Release).filter(Release.product_id == product_model.id).one()
    )

    assert release_model

    canary_py_client = CanaryPyClient(base_url=canarypy_base_url)

    canary_py_client.send_signal_to_canary(
        artifact_url, first_version, instance_id, description, "success"
    )

    signal_model = (
        db_session.query(Signal).filter(Signal.release_id == release_model.id).one()
    )

    assert signal_model

    stable_version = canary_py_client.get_latest_stable_version(product_name)

    assert stable_version == first_version
