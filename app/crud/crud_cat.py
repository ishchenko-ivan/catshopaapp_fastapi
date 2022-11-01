# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from typing import List

from app.crud.base import CRUDBase
from app.models.cat import Cat
from app.schemas.cat import CatCreate, CatUpdate


class CRUDCat(CRUDBase[Cat, CatUpdate, CatCreate]):
    async def get_multi_by_name(
            self, db: AsyncSession, *, name: str, limit: int
) -> List[Cat]:
        # case-insensitive query that doesn't need full-length name
        q = select(self.model).filter( (func.lower(self.model.name)).contains(func.lower(name)) ).limit(limit)
        query = await db.execute(q)
        return query.scalars().all()


cat = CRUDCat(Cat)
