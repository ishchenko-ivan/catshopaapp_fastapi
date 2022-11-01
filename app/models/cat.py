from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.customer import Customer


class Cat(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    description = Column(String(512), index=True, nullable=True)
    status = Column(String(64), nullable=True)
    owner_id = Column(Integer, ForeignKey("customer.id"), nullable=True)
    owner = relationship("Customer", back_populates="cats")