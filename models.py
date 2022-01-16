from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List, Optional


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


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    name: str
    email: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


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


class Order(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    user: User
    order_date: str
    foods: List[Food]
    user_note: Optional[str] = None
    order_date: Optional[str] = None

    def __init__(self):
        super()

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
