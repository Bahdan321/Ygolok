import uuid

from sqlalchemy import UUID, ForeignKey, String, Boolean, Column
from db.models.base_model import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    patronymic = Column(String, nullable=True)
    phone = Column(String, nullable=False, unique=True)
    password_id = Column(UUID(as_uuid=True), ForeignKey("passwords.id"))
    avatar = Column(String, nullable=True)
    is_verified = Column(Boolean, nullable=False)
