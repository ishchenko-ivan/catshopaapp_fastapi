from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Customer(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    second_name = Column(String(256), nullable=True)
    email = Column(String(64), index=True, nullable=False)
    phone = Column(String(32), index=True, nullable=True)
    is_donator = Column(Boolean, default=False)
    cats = relationship(
        "Cat",
        cascade="all",
        back_populates="owner",
        uselist=True
    )