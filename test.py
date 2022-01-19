from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Test get_orders: Get all orders
def test_get_orders():
    response = client.get("/orders")
    assert response.status_code == 200

    response_json = response.json()

    assert "orders" in response_json
    assert "completed" in response_json["orders"]
    assert "not_completed" in response_json["orders"]


# Test get_orders: Get all completed orders
def test_get_completed_orders():
    response = client.get("/orders?t=1")
    assert response.status_code == 200

    response_json = response.json()

    assert "orders" in response_json
    assert "completed" not in response_json["orders"]
    assert "not_completed" not in response_json["orders"]


# Test get_orders: Get all incomplete orders
def test_get_not_completed_orders():
    response = client.get("/orders?t=-1")
    assert response.status_code == 200

    response_json = response.json()

    assert "orders" in response_json
    assert "completed" not in response_json["orders"]
    assert "not_completed" not in response_json["orders"]


# Test get_orders: Call get_orders with invalid parameter
def test_get_orders_with_bad_param():
    response = client.get("/orders?t=5")
    assert response.status_code == 400


# Test get_orders: Call get_orders with invalid parameter
def test_random_endpoint():
    response = client.get("/foo")
    assert response.status_code == 404


# Test get_orders: Get all orders
def test_get_orders():
    response = client.post("/orders/")
    assert response.status_code == 405

