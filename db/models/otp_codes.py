from sqlalchemy import UUID, ForeignKey, String, Column, TIMESTAMP, Boolean, Integer
from db.models.base_model import Base
from sqlalchemy.ext.declarative import as_declarative
import uuid
from datetime import datetime


@as_declarative()
class Otp_codes(Base):
    __tablename__ = "otp_codes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    otp_code = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    status = Column(Boolean, nullable=False)
    failed_count = Column(Integer, nullable=False)
