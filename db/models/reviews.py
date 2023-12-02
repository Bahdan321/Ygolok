import uuid

from datetime import datetime
from sqlalchemy import UUID, ForeignKey, String, Column, TIMESTAMP
from db.models.base_model import Base


class Reviews(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    org_id = Column(UUID, ForeignKey("organizations.id"), nullable=False)
    body = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)