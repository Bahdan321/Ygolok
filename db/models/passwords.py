import uuid

from sqlalchemy import UUID, ForeignKey, String, Column
from db.models.base_model import Base


class Passwords(Base):
    __tablename__ = "passwords"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"))
    password = Column(String, nullable=False)
