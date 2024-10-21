from fastapi.testclient import TestClient

def test_create_item(client):
    response = client.post(
        "/api/v1/items/",
        json={"name": "Test Item", "description": "This is a test item"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "This is a test item"
    assert "id" in data

def test_read_item(client):
    # First, create an item
    response = client.post(
        "/api/v1/items/",
        json={"name": "Test Item", "description": "This is a test item"},
    )
    created_item = response.json()

    # Then, read the item
    response = client.get(f"/api/v1/items/{created_item['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "This is a test item"
    assert data["id"] == created_item["id"]