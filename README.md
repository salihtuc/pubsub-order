# Simple Order REST Service
This repo demonstrates a simple REST API with **Order** example.

The user can do following operations with this API:
- List all (completed/waiting) orders in the system.
- Create new order
- Complete an order

In order to complete these operations, the user can use following API endpoints (with their methods), respectively:
- GET /orders
- POST /orders/new
- POST /orders/complete

You can run the service using:
```uvicorn main:app --reload```
command in a directory, after extracting the content to the directory.

## GET /orders?[t=<order_type>]
This endpoint is using in order to get all *completed* and/or *waiting* orders in the system. 

### Parameters
1. Order Type (t) (Query Parameter) (Optional)
**t** is the type of the order. 
User can specify a value which is one of the numbers in [-1, 0, 1]
**0** is the default value for **t**.

####Options (<order_type>)
- t = 0
The default value. It represents all orders (completed + waiting)

- t = 1
This value is using for getting *completed* orders.

- t = -1
This value is using for getting *waiting* orders.

## POST /orders/new
This endpoint is using for creating new order in the system. The created order goes directly to the queue.

It accepts an **Order** object in JSON format as parameter.

It produces a JSON message from the queue system.

#### Input Example
```
{
    "user": {
        "id": "61e31b1f86d743ba1781db6f",
        "name": "Uğur Ozi",
        "email": "uozy@yspt.com"
    },
    "order_date": "2022-01-16 20:11:22.263795",
    "foods": [
        {
            "id": "61e355f32be1ae938189c3b0",
            "restaurant": "61e31e7139103e5969baa475",
            "name": "Döner",
            "category": "61e3556e03f5bac9f7611b1a",
            "unit_price": 17.5,
            "count": 1
        },
        {
            "id": "61e355f32be1ae938189c3b2",
            "restaurant": "61e31e7139103e5969baa475",
            "name": "Etibol İskender",
            "category": "61e3556e03f5bac9f7611b1a",
            "unit_price": 30.0,
            "count": 1
        }
    ],
    "user_note": "asd"
}
```

#### Output Example
```
{
    "response": {
        "MD5OfMessageBody": "244504cd1a717a3850e8adf1ae0bb83e",
        "MessageId": "63a5329b-4d35-4b34-9ec0-25821d88f3ba",
        "ResponseMetadata": {
            "RequestId": "0ec39e14-d804-5da4-8180-c477a98a6511",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": "0ec39e14-d804-5da4-8180-c477a98a6511",
                "date": "Thu, 20 Jan 2022 14:18:54 GMT",
                "content-type": "text/xml",
                "content-length": "378"
            },
            "RetryAttempts": 0
        }
    }
}
```

## POST /orders/complete
This endpoint is using for completing an order from the queue.

It accepts no parameters and produces a simple JSON object if the operation is successful.

#### Output Example
```
{"success": True}
```

# System Details

This REST endpoint developed with **Fast API** framework in Python.

We are using **MongoDB** for the database operations and **Amazon SQS** for the queue.

## Database Collections
###categories
It represents food categories.

- _id: ObjectId
- name: String

###foods
It represents foods in the system.

- _id: ObjectId
- name: String
- unit_price: Double
- category: ObjectId
- restaurant: ObjectId

###orders
Order object in the system.

- _id: ObjectId
- user: User
- order_date: DateString
- foods: List[Food]
- user_note: String
- complete_date: DateString

###queue
Same as **Order** object, but for incomplete ones just for data-safety purposes. 

- _id: ObjectId
- user: User
- order_date: DateString
- foods: List[Food]
- user_note: String
- complete_date: DateString

###restaurants
- _id: ObjectId
- name: String
- email: String
- address: String

###users
- _id: ObjectId
- name: String
- email: String
