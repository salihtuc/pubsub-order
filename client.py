from models import Order, Food, User
import requests
import datetime
import json

from pymongo import MongoClient

dbname = "order-db"
username = "dbuser"
password = "userDB95"

conn_string = "mongodb+srv://{}:{}@cluster1.fonyr.mongodb.net/{}?retryWrites=true&w=majority".format(username, password, dbname)

print(conn_string)

client = MongoClient(conn_string)
db = client[dbname]

col_foods = db["foods"]
col_users = db["users"]
col_queue = db["queue"]

foods = [x for x in col_foods.find()]
users = [x for x in col_users.find()]

foods[0].update({"count": 1})
foods[2].update({"count": 2})

food_list = list()
food_list.append(foods[0])
food_list.append(foods[2])

the_order = col_queue.find_one(filter={"_id": order_id})

order = Order(user=User(**users[0]), order_date=str(datetime.datetime.now()), foods=food_list)

server_url = 'http://127.0.0.1:8000/orders/new'
res = requests.post(server_url, data=order.json())

assert res.status_code == 200
