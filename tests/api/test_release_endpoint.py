
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
    assert product["semver_version"] == "0.0.2"