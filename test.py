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
    simple_input = {
        "user": {
            "id": "61e31b1f86d743ba1781db6f",
            "name": "U\\u011fur \\u00d6zi",
            "email": "uozy@yspt.com"
        },
        "order_date": "2022-01-16 20:11:22.263795",
        "foods": [
            {
                "id": "61e355f32be1ae938189c3b0",
                "restaurant": "61e31e7139103e5969baa475",
                "name": "D\\u00f6ner",
                "category": "61e3556e03f5bac9f7611b1a",
                "unit_price": 17.5,
                "count": 1
            },
            {
                "id": "61e355f32be1ae938189c3b2",
                "restaurant": "61e31e7139103e5969baa475",
                "name": "Etibol \\u0130skender",
                "category": "61e3556e03f5bac9f7611b1a",
                "unit_price": 30.0,
                "count": 1
            }
        ],
        "user_note": "asd"
    }

    response = client.post("/orders/new", json=simple_input)
    assert response.status_code == 200

    response_json = response.json()

    assert "response" in response_json
    assert "MessageId" in response_json["response"]


# Test new_order: Send POST to "New" with empty body
def test_post_order_with_none_body():
    response = client.post("/orders/new", json=None)
    assert response.status_code == 422  # Unprocessable entry


# Test new_order: Send POST to "New" with invalid body
def test_post_order_with_wrong_body():
    response = client.post("/orders/new", json={"foo": "bar"})
    assert response.status_code == 422  # Unprocessable entry


# Test new_order: Send POST to "New" with empty body
def test_post_order_with_empty_body():
    response = client.post("/orders/new")
    assert response.status_code == 422  # Unprocessable entry


# Test complete_order: Complete order orders
# TODO: We may need to check the queue for that testing
def test_post_complete_order():
    response = client.post("/orders/complete")
    assert response.status_code == 200
    assert response.json() == {"success": True}
