from typing import Optional

from fastapi import FastAPI, Query

from pymongo import MongoClient

from models import Order, Food
import datetime
import json
import uvicorn

from sqs_utils import send_message, receive_message

app = FastAPI()

dbname = "order-db"
username = "dbuser"
password = "userDB95"

conn_string = "mongodb+srv://{}:{}@cluster1.fonyr.mongodb.net/{}?retryWrites=true&w=majority".format(username, password, dbname)

print(conn_string)

client = MongoClient(conn_string)
db = client[dbname]

col_orders = db["orders"]
col_foods = db["foods"]
col_users = db["users"]
col_restaurants = db["restaurants"]
col_categories = db["categories"]
col_queue = db["queue"]


# TODO: We may add type in str or another endpoint
# TODO: We may add date interval for filtering
@app.get("/orders/")
async def get_orders(t: Optional[int] = Query(0)):

    # t = 0 -> all
    # t = -1 -> not completed
    # t = 1 -> completed

    if t == 0:
        completed = [Order(**x) for x in col_orders.find()]
        not_completed = [Order(**x) for x in col_queue.find()]

        return {"orders": {"completed": completed, "not_completed": not_completed}}

    elif t == 0:
        orders = [Order(**x) for x in col_queue.find()]

        return {"orders": orders}

    elif t == 1:
        orders = [Order(**x) for x in col_orders.find()]

        return {"orders": orders}


@app.get("/foods")
async def get_foods():
    foods = [Food(**x) for x in col_foods.find()]
    print(foods)

    return {"foods": foods}


@app.post("/orders/new")
async def create_order(order: Order):

    print("------->")
    print(order)

    rec = col_queue.insert_one(order.dict())

    print(rec.inserted_id)

    order_dict = order.dict()

    order_dict.update({'_id': rec.inserted_id})
    order_dict.update({'inserted_id': rec.inserted_id})

    updated_order = Order.parse_obj(order_dict)

    results = {"order": updated_order}

    print("Message is sending...")
    send_message(updated_order.json())

    return results


@app.post("/orders/complete")
async def complete_order():

    msg = receive_message()

    if msg is None:
        err_msg = "Something went wrong when getting the message. Operation failed."
        print(err_msg)
        return err_msg

    print("Message Received.")
    print(msg)

    the_order = Order(**json.loads(msg))

    if the_order is None:
        return "Failed to get Order object from the message."

    col_queue.delete_one(filter={"_id": the_order.dict()["inserted_id"]})

    print("Deleted")

    order_dict = the_order.dict()

    order_dict.update({"complete_date": str(datetime.datetime.now())})

    col_orders.insert_one(order_dict)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
