from sqlalchemy import Column,  String, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.catcustomer import catcustomer_table


class Cat(Base):
    __tablename__ = "cat"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    description = Column(String(512), index=True, nullable=True)
    status = Column(String(64), nullable=True)

    customers = relationship(
        "Customer",
        secondary=catcustomer_table,
        back_populates="cats"
    )

    # backref='Cat'?