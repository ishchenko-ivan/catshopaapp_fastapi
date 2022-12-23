# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from typing import List

from app.crud.base import CRUDBase
from app.models import Cat, Customer
from app.schemas.cat import CatCreate, CatUpdate


class CRUDCat(CRUDBase[Cat, CatUpdate, CatCreate]):

    def get_multi_by_name(
            self, db: Session, *, name: str = "", limit: int = 10
    ) -> List[Cat]:
        # case-insensitive query that doesn't need full-length name
        q = select(self.model).filter( (func.lower(self.model.name)).contains(func.lower(name)) ).limit(limit)
        # query = await db.execute(q)
        query = db.execute(q)
        return query.scalars().all()

    def add_owner(
            self, db: Session, *, cat_obj: Cat, owner_obj: Customer
    ) -> Cat:
        if owner_obj not in cat_obj.customers:
            # cat_owners.append(owner_obj.id)
            # setattr(cat_obj, "customers", cat_owners)
            cat_obj.customers.append(owner_obj)
            db.add(cat_obj)
            db.commit()
            db.refresh(cat_obj)
            return cat_obj
        else:
            return None

    def remove_owner(
            self, db: Session, *, cat_obj: Cat, owner_obj: Customer
    ) -> Cat:
        if owner_obj in cat_obj.customers:
            cat_obj.customers.remove(owner_obj)
            db.add(cat_obj)
            db.commit()
            db.refresh(cat_obj)
            return cat_obj
        else:
            return None


cat = CRUDCat(Cat)
