from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING

# if TYPE_CHECKING:
#     from app.schemas.cat import CatInDBBase


class CustomerBase(BaseModel):
    name: str
    age: Optional[int]
    email: str
    password: str


class CustomerCreate(CustomerBase):
    pass


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


from app.schemas.cat import CatInDBBase
CustomerInDBBase.update_forward_refs()


# Properties to return to client
class Customer(CustomerInDBBase):
    pass


# Full properties to return to client
class CustomerFull(Customer):
    cats: "List[Optional[CatInDBBase]]"

