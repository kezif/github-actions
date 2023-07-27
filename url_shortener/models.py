from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from .database import Base
#created_at = Column(DateTime, server_default=func.now())


'''class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
'''


class Url(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    shorten_url = Column(String, index=True)
    created_at = Column(DateTime, server_default=func.now())
    clicks = Column(Integer, default=0, index=True)
    #owner_id = Column(Integer, ForeignKey("users.id"))

    #owner = relationship("User", back_populates="items")
