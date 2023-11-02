from sqlalchemy import UUID, ForeignKey, String, Column
from .base import Base

import uuid


class Admins(Base):
    __tablename__ = "admins"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("Users.id"), nullable=False)
    org_id = Column(UUID, ForeignKey("Organizations.id"), nullable=False)
    email = Column(String, nullable=False)
    social_networks = Column(String, nullable=False)