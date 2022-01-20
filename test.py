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
def test_post_orders():
    response = client.post("/orders/")
    assert response.status_code == 405


# Test new_order: Send GET to "New" endpoint
def test_get_new_order():
    response = client.get("/orders/new/")
    assert response.status_code == 405


# Test new_order: Send POST to "New" with valid body
def test_post_order():
    # TODO add true json here
    response = client.post("/orders/new", json={})
    assert response.status_code == 200

    response_json = response.json()

    assert "response" in response_json
    assert "user" in response_json["response"]
    assert "order_date" in response_json["response"]
    assert "foods" in response_json["response"]


# Test new_order: Send POST to "New" with invalid body
def test_post_order_with_wrong_body():
    response = client.post("/orders/new", json={"foo": "bar"})
    assert response.status_code == 500  # TODO: Add the response code


# Test new_order: Send POST to "New" with empty body
def test_post_order_with_empty_body():
    response = client.post("/orders/new")
    assert response.status_code == 400
    assert response.json() == {"error": "Cannot get the input Order from the client."}


# Test complete_order: Complete order orders
# TODO: We may need to check the queue for that testing
def test_post_complete_order():
    response = client.post("/orders/complete")
    assert response.status_code == 200
    assert response.json() == {"success": True}
