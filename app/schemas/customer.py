from pydantic import BaseModel
from typing import Optional, List


class CustomerBase(BaseModel):
    name: str
    age: Optional[int]
    email: str
    password: str


class CustomerCreate(CustomerBase):
    name: str
    age: Optional[int]
    email: str
    password: str


class CustomerUpdate(CustomerBase):
    name: Optional[str]
    age: Optional[int]
    email: Optional[str]
    password: Optional[str]


# Properties shared by models stored in DB
class CustomerInDBBase(CustomerBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Customer(CustomerInDBBase):
    pass
