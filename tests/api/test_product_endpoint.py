

def test_create_and_get_product(client):
    new_product = {
        "description": "My Product",
        "repository_url": "https://github.com/my-product",
        "artifact_url": "https://github.com/my-product/releases/v1.0.0"
    }
    response = client.post("/product", json=new_product)
    product_id = response.json()["id"]
    response = client.get(f"/product/{product_id}")
    assert response.status_code == 200
    product = response.json()
    assert product["description"] == "My Product"
    assert product["repository_url"] == "https://github.com/my-product"
    assert product["artifact_url"] == "https://github.com/my-product/releases/v1.0.0"
