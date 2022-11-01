from pydantic import BaseModel
from typing import Optional

from typing import Sequence

class CatBase(BaseModel):
    name: str
    description: str
    status: str

class CatCreate(CatBase):
    name: str
    description = str
    status = str
    owner_id: Optional[int]

class CatUpdate(CatBase):
    name: str

# Properties shared by models stored in DB
class CatInDBBase(CatBase):
    id: int
    owner_id: Optional[int]

    class Config:
        orm_mode = True


# Properties to return to client
class Cat(CatInDBBase):
    pass
