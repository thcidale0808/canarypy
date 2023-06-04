import datetime
from unittest.mock import patch
from canarypy.api.models.signal import Signal
from sqlalchemy import func
from canarypy.api.models.release import ReleaseCanaryBand


def test_create_release_with_no_signal(client):
    new_product = {
        "name": "product",
        "repository_url": "https://github.com/my-product",
        "artifact_url": "https://github.com/my-product/releases/v1.0.0"
    }
    client.post("/product", json=new_product)

    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.1",
        "is_canary": False,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2
    }
    response = client.post("/release", json=new_release)
    assert response.status_code == 201

    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.2",
        "is_canary": True,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2
    }
    response = client.post("/release", json=new_release)
    assert response.status_code == 201

    response = client.get(f"/release/product/latest")
    assert response.status_code == 200
    product = response.json()
    assert product['product']["artifact_url"] == "https://github.com/my-product/releases/v1.0.0"
    assert product['product']["name"] == "product"
    assert product["semver_version"] == "0.0.2"


def test_create_release_with_success_signal(client):
    new_product = {
        "name": "product",
        "repository_url": "https://github.com/my-product",
        "artifact_url": "https://github.com/my-product/releases/v1.0.0"
    }
    client.post("/product", json=new_product)

    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.1",
        "is_canary": False,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2
    }
    response = client.post("/release", json=new_release)
    assert response.status_code == 201
    new_signal = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.1",
        "instance_id": "123",
        "description": "My signal",
        "status": "success"
    }
    response = client.post("/signal", json=new_signal)

    assert response.status_code == 201
    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.2",
        "is_canary": True,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2
    }
    response = client.post("/release", json=new_release)
    assert response.status_code == 201

    response = client.get(f"/release/product/latest")
    assert response.status_code == 200
    product = response.json()
    assert product['product']["artifact_url"] == "https://github.com/my-product/releases/v1.0.0"
    assert product['product']["name"] == "product"
    assert product["semver_version"] == "0.0.2"


def test_create_release_with_canary_success_signal(client):
    new_product = {
        "name": "product",
        "repository_url": "https://github.com/my-product",
        "artifact_url": "https://github.com/my-product/releases/v1.0.0"
    }
    client.post("/product", json=new_product)

    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.1",
        "is_canary": False,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2
    }
    response = client.post("/release", json=new_release)
    assert response.status_code == 201

    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.2",
        "is_canary": True,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2
    }
    response = client.post("/release", json=new_release)
    assert response.status_code == 201

    new_signal = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.2",
        "instance_id": "123",
        "description": "My signal",
        "status": "success"
    }
    response = client.post("/signal", json=new_signal)

    response = client.get(f"/release/product/latest")
    assert response.status_code == 200
    product = response.json()
    assert product['product']["artifact_url"] == "https://github.com/my-product/releases/v1.0.0"
    assert product['product']["name"] == "product"
    assert product["semver_version"] == "0.0.1"


def test_create_release_with_both_success_signal(client):
    new_product = {
        "name": "product",
        "repository_url": "https://github.com/my-product",
        "artifact_url": "https://github.com/my-product/releases/v1.0.0"
    }
    client.post("/product", json=new_product)

    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.1",
        "is_canary": False,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2
    }
    response = client.post("/release", json=new_release)
    assert response.status_code == 201
    new_signal = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.1",
        "instance_id": "123",
        "description": "My signal",
        "status": "success"
    }
    response = client.post("/signal", json=new_signal)
    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.2",
        "is_canary": True,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2
    }
    response = client.post("/release", json=new_release)
    assert response.status_code == 201

    new_signal = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.2",
        "instance_id": "123",
        "description": "My signal",
        "status": "success"
    }
    response = client.post("/signal", json=new_signal)

    response = client.get(f"/release/product/latest")
    assert response.status_code == 200
    product = response.json()
    assert product['product']["artifact_url"] == "https://github.com/my-product/releases/v1.0.0"
    assert product['product']["name"] == "product"
    assert product["semver_version"] == "0.0.1"


def test_release_with_correct_proportion_of_canary_signals(client):
    new_product = {
        "name": "product",
        "repository_url": "https://github.com/my-product",
        "artifact_url": "https://github.com/my-product/releases/v1.0.0"
    }
    client.post("/product", json=new_product)

    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.1",
        "is_canary": False,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2
    }
    response = client.post("/release", json=new_release)
    assert response.status_code == 201
    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.2",
        "is_canary": True,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2
    }
    response = client.post("/release", json=new_release)
    results = {}
    for i in range(0, 100):
        release = client.get(f"/release/product/latest").json()
        new_signal = {
            "artifact_url": "https://github.com/my-product/releases/v1.0.0",
            "semver_version": release["semver_version"],
            "instance_id": "123",
            "description": "My signal",
            "status": "success"
        }
        client.post("/signal", json=new_signal)
        if release["semver_version"] not in results:
            results[release["semver_version"]] = 0
        results[release["semver_version"]] += 1
    assert results["0.0.1"] == 80
    assert results["0.0.2"] == 20


def test_release_with_canary_period_with_all_bands_populated(client, db_session):
    new_product = {
        "name": "product",
        "repository_url": "https://github.com/my-product",
        "artifact_url": "https://github.com/my-product/releases/v1.0.0"
    }
    client.post("/product", json=new_product)

    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.1",
        "is_canary": False,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2
    }
    response = client.post("/release", json=new_release)

    assert response.status_code == 201
    with patch('datetime.datetime', wraps=datetime.datetime) as mock_datetime:
        desired_timestamp = datetime.datetime(2023, 1, 1, 10, 30, 0)
        mock_datetime.now.return_value = desired_timestamp
        new_release = {
            "artifact_url": "https://github.com/my-product/releases/v1.0.0",
            "semver_version": "0.0.2",
            "is_canary": True,
            "is_active": True,
            "threshold": 80,
            "canary_period": 2,
            "release_date": desired_timestamp.isoformat()
        }
        response = client.post("/release", json=new_release)
        results = {}

        for i in range(0, 600):
            if i % 100 == 0 and i != 0:
                desired_timestamp += datetime.timedelta(days=(2/5+1/2000))
            mock_datetime.now.return_value = desired_timestamp
            release = client.get(f"/release/product/latest").json()
            new_signal = {
                "artifact_url": "https://github.com/my-product/releases/v1.0.0",
                "semver_version": release["semver_version"],
                "instance_id": "123",
                "description": "My signal",
                "status": "success"
            }
            client.post("/signal", json=new_signal)
            if release["semver_version"] not in results:
                results[release["semver_version"]] = 0
            results[release["semver_version"]] += 1
    assert results["0.0.1"] == 201
    assert results["0.0.2"] == 399


def test_release_created_with_signals_linked_to_release_bands(client, db_session):
    new_product = {
        "name": "product",
        "repository_url": "https://github.com/my-product",
        "artifact_url": "https://github.com/my-product/releases/v1.0.0"
    }
    client.post("/product", json=new_product)

    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "0.0.1",
        "is_canary": False,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2
    }
    response = client.post("/release", json=new_release)
    expected_first_release_id = response.json().get('id')
    assert response.status_code == 201
    with patch('datetime.datetime', wraps=datetime.datetime) as mock_datetime:
        desired_timestamp = datetime.datetime(2023, 1, 1, 10, 30, 0)
        mock_datetime.now.return_value = desired_timestamp
        new_release = {
            "artifact_url": "https://github.com/my-product/releases/v1.0.0",
            "semver_version": "0.0.2",
            "is_canary": True,
            "is_active": True,
            "threshold": 80,
            "canary_period": 2,
            "release_date": desired_timestamp.isoformat()
        }
        response = client.post("/release", json=new_release)
        expected_second_release_id = response.json().get('id')
        results = {}

        for i in range(0, 100):
            if i % 20 == 0 and i != 0:
                desired_timestamp += datetime.timedelta(days=(2 / 5 + 1 / 20000))
            mock_datetime.now.return_value = desired_timestamp
            release = client.get(f"/release/product/latest").json()
            new_signal = {
                "artifact_url": "https://github.com/my-product/releases/v1.0.0",
                "semver_version": release["semver_version"],
                "instance_id": "123",
                "description": "My signal",
                "status": "success"
            }
            client.post("/signal", json=new_signal)
            if release["semver_version"] not in results:
                results[release["semver_version"]] = 0
            results[release["semver_version"]] += 1
        new_release = {
            "artifact_url": "https://github.com/my-product/releases/v1.0.0",
            "semver_version": "0.0.3",
            "is_canary": True,
            "is_active": True,
            "threshold": 80,
            "canary_period": 2,
            "release_date": desired_timestamp.isoformat()
        }
        response = client.post("/release", json=new_release)
        expected_third_release_id = response.json().get('id')
        results = {}

        for i in range(0, 100):
            if i % 20 == 0 and i != 0:
                desired_timestamp += datetime.timedelta(days=(2 / 5 + 1 / 20000))
            mock_datetime.now.return_value = desired_timestamp
            release = client.get(f"/release/product/latest").json()
            new_signal = {
                "artifact_url": "https://github.com/my-product/releases/v1.0.0",
                "semver_version": release["semver_version"],
                "instance_id": "123",
                "description": "My signal",
                "status": "success"
            }
            client.post("/signal", json=new_signal)
            if release["semver_version"] not in results:
                results[release["semver_version"]] = 0
            results[release["semver_version"]] += 1

    signals_first_release_count = db_session.query(func.count(Signal.id)).join(
        ReleaseCanaryBand, Signal.release_canary_band_id == ReleaseCanaryBand.id
    ).filter(
        (Signal.release_id == expected_first_release_id) & (ReleaseCanaryBand.band_number == 1)
    ).scalar()

    signals_second_release_count = db_session.query(func.count(Signal.id)).join(
        ReleaseCanaryBand, Signal.release_canary_band_id == ReleaseCanaryBand.id
    ).filter(
        (Signal.release_id == expected_second_release_id) & (ReleaseCanaryBand.band_number == 1)
    ).scalar()

    signals_third_release_count = db_session.query(func.count(Signal.id)).join(
        ReleaseCanaryBand, Signal.release_canary_band_id == ReleaseCanaryBand.id
    ).filter(
        (Signal.release_id == expected_third_release_id) & (ReleaseCanaryBand.band_number == 1)
    ).scalar()

    assert signals_first_release_count == 16
    assert signals_second_release_count == 20
    assert signals_third_release_count == 4
