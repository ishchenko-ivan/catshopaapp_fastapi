# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from typing import List

import app.models
from app.crud.base import CRUDBase
from app.models import Customer, Cat
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CRUDCustomer(CRUDBase[Customer, CustomerUpdate, CustomerCreate]):

    def get_multi_by_name(
            self, db: Session, *, name: str, limit: int
    ) -> List[Customer]:
        # case-insensitive query that doesn't need full-length name
        q = select(self.model).filter( (func.lower(self.model.name)).contains(func.lower(name)) ).limit(limit)
        query = db.execute(q)
        return query.scalars().all()

    def get_multi_by_cat_name(
            self, db: Session, *, cat_name: str, limit: int
    ) -> List[Customer]:

        q = select(self.model).join(Cat.customers).filter(cat_name == Cat.name).limit(limit)
        query = db.execute(q)
        return query.scalars().all()

    def add_cat(
            self, db: Session, *, customer_obj: Customer, cat_obj: Cat
    ) -> Customer:
        if cat_obj not in customer_obj.cats:
            # cat_owners.append(owner_obj.id)
            # setattr(cat_obj, "customers", cat_owners)
            customer_obj.cats.append(cat_obj)
            db.add(customer_obj)
            db.commit()
            db.refresh(customer_obj)
            return customer_obj
        else:
            return None

    def remove_cat(
            self, db: Session, *, customer_obj: Customer, cat_obj: Cat
    ) -> Customer:
        if cat_obj in customer_obj.cats:
            customer_obj.cats.remove(cat_obj)
            db.add(customer_obj)
            db.commit()
            db.refresh(customer_obj)
            return customer_obj
        else:
            return None


customer = CRUDCustomer(Customer)
