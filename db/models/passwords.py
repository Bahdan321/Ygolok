import uuid

from sqlalchemy import UUID, String, Column
from db.models.base_model import Base


class Passwords(Base):
    __tablename__ = "passwords"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    password = Column(String, nullable=False)
