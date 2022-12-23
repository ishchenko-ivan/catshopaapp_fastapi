from pydantic import BaseModel
from typing import Optional, List


class CatBase(BaseModel):
    name: str
    description: str
    status: str


class CatCreate(CatBase):
    pass


class CatUpdate(CatBase):
    name: Optional[str]
    description: Optional[str]
    status: Optional[str]


# Properties shared by models stored in DB
class CatInDBBase(CatBase):
    id: int

    class Config:
        orm_mode = True


from app.schemas.customer import CustomerInDBBase
CatInDBBase.update_forward_refs()


# Properties to return to client
class Cat(CatInDBBase):
    pass


# Full properties to return to client
class CatFull(Cat):
    customers: "List[Optional[CustomerInDBBase]]"





