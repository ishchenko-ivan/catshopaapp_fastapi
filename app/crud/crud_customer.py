from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from typing import List

from app.crud.base import CRUDBase
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CRUDCustomer(CRUDBase[Customer, CustomerUpdate, CustomerCreate]):
    async def get_multi_by_cat_name(
            self, db: AsyncSession, *, cat_name: str, limit: int
) -> List[Customer]:
        # case-insensitive query that doesn't need full-length name
        # q = select(self.model).filter( (func.lower(self.model.name)).contains(func.lower(name)) ).limit(limit)
        # query = await db.execute(q)
        # return query.scalars().all()
        pass


customer = CRUDCustomer(Customer)
