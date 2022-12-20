from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.catcustomer import catcustomer


class Customer(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    age = Column(Integer, nullable=True)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=True)

    cats = relationship(
        "Cat",
        secondary=catcustomer,
        back_populates="customers",
    )

    # backref='Customer'?