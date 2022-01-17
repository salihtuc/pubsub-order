from typing import Optional

from fastapi import FastAPI, Query

from pymongo import MongoClient

from models import Order, Food, PyObjectId
import datetime

from sqs_try import send_message, receive_message

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
@app.get("/orders/")
async def get_orders(t: Optional[int] = Query(-1)):

    if t == -1:
        orders = [Order(**x) for x in col_orders.find()]

        return {"orders": orders}
    elif t == 0:
        orders = [Order(**x) for x in col_queue.find()]

        return {"orders": [o for o in orders if o.status == 'In Progress']}


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

    order.dict().update({'inserted_id': rec.inserted_id})

    results = {"order": order}

    print("Message is sending...")
    send_message(order.json())

    return results


@app.post("/orders/complete")
async def complete_order():

    #the_order = col_queue.find_one(filter={"_id": order_id})

    msg = receive_message()

    print("Message Received.")
    print(msg)

    #the_order = col_queue.find_one(filter={})

    the_order = Order(**msg)

    if the_order is None:
        return None

    #print(the_order)
    #print(Order(**the_order))

    #return order_id

    col_queue.delete_one(filter={"_id": the_order.dict()["id"]})

'''
    print("Deleted")

    Order(**the_order).dict().update({"complete_date": str(datetime.datetime.now())})

    col_orders.insert_one(Order(**the_order).dict())
'''


