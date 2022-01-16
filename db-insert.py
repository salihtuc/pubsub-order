from pymongo import MongoClient

dbname = "order-db"
username = "dbuser"
password = "userDB95"

conn_string = "mongodb+srv://{}:{}@cluster1.fonyr.mongodb.net/{}?retryWrites=true&w=majority".format(username, password, dbname)

print(conn_string)

client = MongoClient(conn_string)
db = client[dbname]

col_queue = db["queue"]
col_orders = db["orders"]
col_foods = db["foods"]
col_users = db["users"]
col_restaurants = db["restaurants"]
col_categories = db["categories"]

'''
u1 = {
    "userId": 1,
    "name": "Uğur Özi",
    "email": "uozy@yspt.com"
}

u2 = {
    "userId": 2,
    "name": "Cenk Yaldız",
    "email": "cyaldiz@yspt.com"
}

u3 = {
    "userId": 3,
    "name": "Selin Simge",
    "email": "ssimge@yspt.com"
}

col_users.insert_many([u1, u2, u3])
'''

'''
r1 = {
    "restaurantId": 1,
    "name": "Süper Dönerci",
    "email": "donerci@yspt.com",
    "address": "0000"
}

r2 = {
    "restaurantId": 2,
    "name": "Harika Ev Yemekleri",
    "email": "harikaev@yspt.com",
    "address": "1111"
}

r3 = {
    "restaurantId": 3,
    "name": "Bizim Büfe",
    "email": "bufe@yspt.com",
    "address": "2222"
}

col_restaurants.insert_many([r1, r2, r3])
'''

'''
c1 = {
    "categoryId": 1,
    "name": "Döner/Kebap"
}

c2 = {
    "categoryId": 2,
    "name": "Ev Yemekleri"
}

c3 = {
    "categoryId": 3,
    "name": "Fast-Food"
}

col_categories.insert_many([c1, c2, c3])
'''

'''
f1 = {
    "foodId": 7,
    "restaurantId": 3,
    "name": "Goralı",
    "categoryId": 3,
    "unit_price": 20
}

f2 = {
    "foodId": 8,
    "restaurantId": 3,
    "name": "Dilli Kaşarlı",
    "categoryId": 3,
    "unit_price": 10
}

f3 = {
    "foodId": 9,
    "restaurantId": 3,
    "name": "Yengen",
    "categoryId": 3,
    "unit_price": 15
}

col_foods.insert_many([f1, f2, f3])
'''

'''
o1 = {
    "user": {
        "name": "Uğur Ozi",
        "email": "uozy@yspt.com"
    },
    "order_date": "2022-01-16 15:21:11.281250",
    "foods": [
        {
            "name": "Döner",
            "unit_price": 17.5,
            "count": 1
        },
        {
            "name": "Etibol İskender",
            "unit_price": 30.0,
            "count": 1
        }
    ],
    "user_note": None
}

col_queue.insert_one(o1)
'''

# col_queue.delete_many({})
