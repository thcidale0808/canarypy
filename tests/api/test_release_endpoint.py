
def test_create_release_with_no_signal(client):
    new_product = {
        "name": "product",
        "repository_url": "https://github.com/my-product",
        "artifact_url": "https://github.com/my-product/releases/v1.0.0"
    }
    client.post("/product", json=new_product)

    new_release = {
        "artifact_url": "https://github.com/my-product/releases/v1.0.0",
        "semver_version": "1.0.0",
        "is_canary": True,
        "is_active": True,
        "threshold": 80,
        "canary_period": 2.0
    }
    response = client.post("/release", json=new_release)
    assert response.status_code == 201

    response = client.get(f"/release/product/latest")
    assert response.status_code == 200
    product = response.json()
    assert product["artifact_url"] == "https://github.com/my-product/releases/v1.0.0"
    assert product["semver_version"] == "1.0.0"
