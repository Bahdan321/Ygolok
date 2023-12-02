import uuid

from sqlalchemy import UUID, ForeignKey, String, Column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from db.models.base_model import Base


class Admins(Base):
    __tablename__ = 'admins'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    org_id = Column(UUID, ForeignKey('organizations.id'), nullable=False)
    email = Column(String, nullable=False)
    social_networks = Column(String, nullable=False)
    user = relationship('Users', backref='user_admin', single_parent=True, innerjoin=True)
