from pydantic import BaseModel
from typing import Optional


class CatBase(BaseModel):
    name: str
    description: str
    status: str


class CatCreate(CatBase):
    name: str
    description = str
    status = str


class CatUpdate(CatBase):
    name: Optional[str]
    description: Optional[str]
    status: Optional[str]


# Properties shared by models stored in DB
class CatInDBBase(CatBase):
    id: int

    class Config:
        orm_mode = True





# Properties to return to client
class Cat(CatInDBBase):
    pass
