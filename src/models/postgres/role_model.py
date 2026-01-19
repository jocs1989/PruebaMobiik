from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from src.models.postgres.user_role_model import user_roles
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String)

    users = relationship(
        "User",
        secondary=user_roles,
        back_populates="roles"
    )
