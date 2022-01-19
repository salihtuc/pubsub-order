from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List, Optional


# This class is using for "_id"-like attributes in Mongo. ObjectId(...) representation
class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


# This class is using for representing User collection in Mongo.
class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    name: str
    email: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


# This class is using for representing Food collection in Mongo.
class Food(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    restaurant: Optional[PyObjectId]
    name: str
    category: Optional[PyObjectId]
    unit_price: float
    count: Optional[int]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


# This class is using for representing Order collection in Mongo.
class Order(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    user: User
    foods: List[Food]
    user_note: Optional[str] = None
    order_date: Optional[str] = None
    complete_date: Optional[str] = None
    inserted_id: Optional[PyObjectId] = None

    def __init__(self):
        super().__init__()

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
