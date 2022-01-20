from typing import Optional
from fastapi import FastAPI, Query, HTTPException
from pymongo import MongoClient

import datetime
import json
import uvicorn

from models import Order, Food
from sqs_utils import send_message, receive_message

# Create the service
app = FastAPI()

# Default connection parameters for MongoDB connection.
dbname = "order-db"
username = "dbdemo"
password = "UFVVRpo3FTcdzrfH"

conn_string = "mongodb+srv://{}:{}@cluster1.fonyr.mongodb.net/{}?retryWrites=true&w=majority".format(username, password,
                                                                                                     dbname)
print(conn_string)

# Get the Mongo Client, DB and collections
client = MongoClient(conn_string)

db = client[dbname]

col_orders = db["orders"]
col_foods = db["foods"]
col_users = db["users"]
col_restaurants = db["restaurants"]
col_categories = db["categories"]
col_queue = db["queue"]


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

    elif t == -1:
        orders = [Order(**x) for x in col_queue.find()]

        return {"orders": orders}

    elif t == 1:
        orders = [Order(**x) for x in col_orders.find()]

        return {"orders": orders}
    else:
        raise HTTPException(status_code=400, detail="{} is not a valid option.".format(t))


@app.get("/foods")
async def get_foods():
    foods = [Food(**x) for x in col_foods.find()]
    print(foods)

    return {"foods": foods}


@app.post("/orders/new")
async def create_order(order: Order):

    if order is None:
        err_msg = "Cannot get the input Order from the client."
        raise HTTPException(status_code=400, detail={"error": err_msg})

    print("------->")
    print(order)

    # TODO: Analyze order; is user in the system, is food in the system, etc.
    # NOTE: For now, we are assuming that the order contains correct data.


    # Insert the order to the queue database in order to prevent data loss.
    rec = col_queue.insert_one(order.dict())

    # Log the id of newly inserted order in queue collection
    print(rec.inserted_id)

    # Get the order object's dict in order to update the model
    order_dict = order.dict()

    # Update dict with inserted order id
    # _id for setting "id" value.
    order_dict.update({'_id': rec.inserted_id})

    # In complete operation, server cannot get the "_id" attribute. So, we are using custom value.
    order_dict.update({'inserted_id': rec.inserted_id})

    # Create new order from updated order dict
    updated_order = Order.parse_obj(order_dict)

    # Prepare return data and send message to the queue

    print("Message is sending...")
    queue_response = send_message(updated_order.json())

    results = {"response": queue_response}

    return results


@app.post("/orders/complete")
async def complete_order():
    msg = receive_message()

    if msg is None:
        err_msg = "Something went wrong when getting the message. Operation failed."
        print(err_msg)
        raise HTTPException(status_code=500, detail=err_msg)

    print("Message Received:")
    print(msg)

    # Get the order from queue message
    the_order = Order(**json.loads(msg))

    if the_order is None:
        err_msg = "Failed to get Order object from the message."
        raise HTTPException(status_code=500, detail=err_msg)

    # Delete the order from queue, because it completed.
    col_queue.delete_one(filter={"_id": the_order.dict()["inserted_id"]})

    print("Deleted: {}".format(the_order.dict()["inserted_id"]))

    # Update the order dict with order completion date
    order_dict = the_order.dict()
    order_dict.update({"complete_date": str(datetime.datetime.now())})

    # Insert the order to the orders table, because it completed.
    col_orders.insert_one(order_dict)

    return {"success": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
