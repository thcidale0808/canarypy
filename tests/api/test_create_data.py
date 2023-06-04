import datetime
import uuid
from unittest.mock import patch

import pytest

BASE_URL = "http://localhost:9090"


def create_product(client, name, repository_url, artifact_url):
    new_product = {
        "name": name,
        "repository_url": repository_url,
        "artifact_url": artifact_url
    }
    client.post(f"{BASE_URL}/product", json=new_product)


def create_signal(client, semver_version, status, artifact_url):
    new_signal = {
        "artifact_url": artifact_url,
        "semver_version": semver_version,
        "instance_id": "123",
        "description": f"My signal {semver_version}",
        "status": status
    }
    client.post(f"{BASE_URL}/signal", json=new_signal)


def create_release(client, semver_version, is_canary, is_active, threshold, canary_period, release_date, product_name, artifact_url):
    new_release = {
        "artifact_url": artifact_url,
        "semver_version": semver_version,
        "is_canary": is_canary,
        "is_active": is_active,
        "threshold": threshold,
        "canary_period": canary_period,
        "release_date": release_date.isoformat()
    }
    client.post(f"{BASE_URL}/release", json=new_release)

    create_release_data(client, 600, 100, product_name, release_date, artifact_url)
    print(f"Created release {semver_version} and release data.")


def create_release_data(client, total_signals, band_size, product_name, reference_date, artifact_url):
    desired_date = reference_date
    with patch('datetime.datetime', wraps=datetime.datetime) as mock_datetime:
        mock_datetime.now.return_value = desired_date
        for i in range(0, total_signals):
            if i % band_size == 0 and i != 0:
                desired_date += datetime.timedelta(days=(2/5+1/2000))
            mock_datetime.now.return_value = desired_date
            release = client.get(f"{BASE_URL}/release/{product_name}/latest").json()
            if release:
                create_signal(client, release["semver_version"], "success", artifact_url)


def generate_uuid():
    return str(uuid.uuid4())


def create_releases(client, releases_number, product_name, artifact_url):
    interval_releases = 7
    desired_timestamp = datetime.datetime(2023, 1, 1, 10, 30, 0)
    for i in range(0, releases_number):
        print(f"Creating release 0.0.{i}")
        create_release(client, f"0.0.{i}", False if i == 0 else True, True, 80, 2, desired_timestamp, product_name, artifact_url)
        desired_timestamp += datetime.timedelta(days=interval_releases)


def create_data(client, product_count: int, release_count_per_product: int):
    for i in range(0, product_count):
        product_name = f"product_{generate_uuid()}"
        artifact_url = f"https://github.com/{product_name}/releases/"
        create_product(client, product_name, artifact_url, artifact_url)
        create_releases(client, release_count_per_product, product_name, artifact_url)


@pytest.mark.skip(reason='This will be converted to a data simulator')
def test_create_data(client):
    create_data(client, 5, 5)
