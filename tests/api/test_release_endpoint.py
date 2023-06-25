import datetime
from unittest.mock import patch

from sqlalchemy import func

from canarypy.api.models.release import ReleaseCanaryBand
from canarypy.api.models.signal import Signal


def test_create_release_with_no_signal(client):
    product_details = {
        "name": "product",
        "repository_url": "https://github.com/my-product",
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
    }

    release_details = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.1",
        "is_canary": False,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2,
    }

    create_product(client, product_details)
    create_release(client, release_details)
    release_details["semver_version"] = "0.0.2"
    release_details["is_canary"] = True
    create_release(client, release_details)
    response = client.get(f"/release/{product_details['name']}/latest")
    assert response.status_code == 200
    product_response = response.json()
    assert (
        product_response["product"]["artifact_url"] == product_details["artifact_url"]
    )
    assert product_response["product"]["name"] == product_details["name"]
    assert product_response["semver_version"] == "0.0.2"


def test_create_release_with_success_signal(client):
    new_product = {
        "name": "product",
        "repository_url": "https://github.com/my-product",
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
    }
    create_product(client, new_product)

    new_release_1 = {
        "artifact_url": new_product["artifact_url"],
        "semver_version": "0.0.1",
        "is_canary": False,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2,
    }
    create_release(client, new_release_1)

    new_signal_1 = {
        "artifact_url": new_product["artifact_url"],
        "semver_version": new_release_1["semver_version"],
        "instance_id": "123",
        "description": "My signal",
        "status": "success",
    }
    response = client.post("/signal", json=new_signal_1)
    assert (
        response.status_code == 201
    ), f"Unexpected status code: {response.status_code}"

    new_release_2 = {
        "artifact_url": new_product["artifact_url"],
        "semver_version": "0.0.2",
        "is_canary": True,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2,
    }
    create_release(client, new_release_2)

    response = client.get(f"/release/{new_product['name']}/latest")
    assert response.status_code == 200
    product_response = response.json()
    assert product_response["product"]["artifact_url"] == new_product["artifact_url"]
    assert product_response["product"]["name"] == new_product["name"]
    assert product_response["semver_version"] == new_release_2["semver_version"]


def test_create_release_with_canary_success_signal(client):
    # Product Creation
    new_product = {
        "name": "product",
        "repository_url": "https://github.com/my-product",
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
    }
    create_product(client, new_product)

    # Creating first release
    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.1",
        "is_canary": False,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2,
    }
    create_release(client, new_release)

    # Creating second release
    new_release["semver_version"] = "0.0.2"
    new_release["is_canary"] = True
    create_release(client, new_release)

    # Sending signal
    new_signal = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.2",
        "instance_id": "123",
        "description": "My signal",
        "status": "success",
    }
    response = client.post("/signal", json=new_signal)
    assert (
        response.status_code == 201
    ), f"Unexpected status code: {response.status_code}"

    # Getting the latest release
    response = client.get(f"/release/product/latest")
    assert response.status_code == 200
    product = response.json()

    assert (
        product["product"]["artifact_url"]
        == "https://github.com/my-product/releases/v1.0.0"
    )
    assert product["product"]["name"] == "product"
    assert product["semver_version"] == "0.0.1"


def test_create_release_with_both_success_signal(client):
    # Product Creation
    new_product = {
        "name": "product",
        "repository_url": "https://github.com/my-product",
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
    }
    create_product(client, new_product)

    # Creating first release
    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.1",
        "is_canary": False,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2,
    }
    create_release(client, new_release)

    # Sending first signal
    new_signal = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.1",
        "instance_id": "123",
        "description": "My signal",
        "status": "success",
    }
    client.post("/signal", json=new_signal)

    # Creating second release
    new_release["semver_version"] = "0.0.2"
    new_release["is_canary"] = True
    create_release(client, new_release)

    # Sending second signal
    new_signal["semver_version"] = "0.0.2"
    client.post("/signal", json=new_signal)

    # Getting the latest release
    response = client.get(f"/release/product/latest")
    assert response.status_code == 200
    product = response.json()

    assert (
        product["product"]["artifact_url"]
        == "https://github.com/my-product/releases/v1.0.0"
    )
    assert product["product"]["name"] == "product"
    assert product["semver_version"] == "0.0.1"


def test_release_with_correct_proportion_of_canary_signals(client):
    # Product Creation
    new_product = {
        "name": "product",
        "repository_url": "https://github.com/my-product",
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
    }
    create_product(client, new_product)

    # Creating first release
    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.1",
        "is_canary": False,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2,
    }
    create_release(client, new_release)

    # Creating second release
    new_release["semver_version"] = "0.0.2"
    new_release["is_canary"] = True
    create_release(client, new_release)

    # Send signals
    results = send_signals(client, datetime.datetime.now(), loop_count=100)

    assert results["0.0.1"] == 80
    assert results["0.0.2"] == 20


def test_release_with_canary_period_with_all_bands_populated(client, db_session):
    new_product = {
        "name": "product",
        "repository_url": "https://github.com/my-product",
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
    }
    create_product(client, new_product)

    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.1",
        "is_canary": False,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2,
    }
    create_release(client, new_release)

    desired_timestamp = datetime.datetime(2023, 1, 1, 10, 30, 0)
    new_release["semver_version"] = "0.0.2"
    new_release["is_canary"] = True
    new_release["release_date"] = desired_timestamp.isoformat()

    operation = lambda mock_datetime: create_release(client, new_release)
    _, mock_datetime = mock_date_and_perform_operation(desired_timestamp, operation)

    send_signals_operation = lambda mock_datetime: send_signals(
        client, desired_timestamp, mock_datetime, 600, 100
    )
    results, _ = mock_date_and_perform_operation(
        desired_timestamp, send_signals_operation
    )

    assert results["0.0.1"] == 201
    assert results["0.0.2"] == 399


def create_product(client, product_data):
    return client.post("/product", json=product_data)


def create_release(client, release_data):
    response = client.post("/release", json=release_data)
    assert response.status_code == 201
    return response.json().get("id")


def mock_date_and_perform_operation(desired_timestamp, operation_func):
    with patch("datetime.datetime", wraps=datetime.datetime) as mock_datetime:
        mock_datetime.now.return_value = desired_timestamp
        result = operation_func(mock_datetime)
    return result, mock_datetime


def send_signals(
    client,
    desired_timestamp,
    mock_datetime=None,
    loop_count=100,
    increment_condition=20,
):
    results = {}
    for i in range(0, loop_count):
        if mock_datetime and i % increment_condition == 0 and i != 0:
            desired_timestamp += datetime.timedelta(days=(2 / 5 + 1 / 20000))
            mock_datetime.now.return_value = desired_timestamp
        release = client.get(f"/release/product/latest").json()
        new_signal = {
            "artifact_url": "https://github.com/my-product/releases/v1.0.0",
            "semver_version": release["semver_version"],
            "instance_id": "123",
            "description": "My signal",
            "status": "success",
        }
        client.post("/signal", json=new_signal)
        if release["semver_version"] not in results:
            results[release["semver_version"]] = 0
        results[release["semver_version"]] += 1
    return results


def count_signals(db_session, release_id):
    return (
        db_session.query(func.count(Signal.id))
        .join(ReleaseCanaryBand, Signal.release_canary_band_id == ReleaseCanaryBand.id)
        .filter(
            (Signal.release_id == release_id) & (ReleaseCanaryBand.band_number == 1)
        )
        .scalar()
    )


def test_release_created_with_signals_linked_to_release_bands(client, db_session):
    new_product = {
        "name": "product",
        "repository_url": "https://github.com/my-product",
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
    }
    create_product(client, new_product)

    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.1",
        "is_canary": False,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2,
    }
    first_release_id = create_release(client, new_release)

    desired_timestamp = datetime.datetime(2023, 1, 1, 10, 30, 0)

    new_release["semver_version"] = "0.0.2"
    new_release["is_canary"] = True
    new_release["release_date"] = desired_timestamp.isoformat()

    operation = lambda mock_datetime: create_release(client, new_release)
    second_release_id, mock_datetime = mock_date_and_perform_operation(
        desired_timestamp, operation
    )

    send_signals_operation = lambda mock_datetime: send_signals(
        client, desired_timestamp, mock_datetime
    )
    results, mock_datetime = mock_date_and_perform_operation(
        desired_timestamp, send_signals_operation
    )

    new_release["semver_version"] = "0.0.3"
    new_release["release_date"] = desired_timestamp.isoformat()

    operation = lambda mock_datetime: create_release(client, new_release)
    third_release_id, mock_datetime = mock_date_and_perform_operation(
        desired_timestamp, operation
    )

    send_signals_operation = lambda mock_datetime: send_signals(
        client, desired_timestamp, mock_datetime
    )
    results, mock_datetime = mock_date_and_perform_operation(
        desired_timestamp, send_signals_operation
    )

    signals_first_release_count = count_signals(db_session, first_release_id)
    signals_second_release_count = count_signals(db_session, second_release_id)
    signals_third_release_count = count_signals(db_session, third_release_id)

    assert signals_first_release_count == 16
    assert signals_second_release_count == 20
    assert signals_third_release_count == 4
