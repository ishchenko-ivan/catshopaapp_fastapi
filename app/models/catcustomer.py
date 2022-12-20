from sqlalchemy import Column, ForeignKey, Table
from app.db.base_class import Base

catcustomer = Table(
    "catcustomer_table",
    Base.metadata,
    Column("cat_id", ForeignKey("cat.id"), primary_key=True),
    Column("customer_id", ForeignKey("customer.id"), primary_key=True)
)
