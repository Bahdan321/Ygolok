from sqlalchemy import UUID, ForeignKey, String, Boolean, Column
from database import Base
from models.passwords import Passwords
import uuid

class Owners(Base):
    __tablename__ = "owners"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    inn = Column(String,nullable=False)
    ogrn = Column(String,nullable=False)
    patronymic = Column(String,nullable=True)
    phone = Column(String,nullable=False,unique=True)
    password_id = Column(UUID,ForeignKey("Passwords.id"),nullable=False)
    avatar = Column(String,nullable=False)
    is_verified = Column(Boolean, nullable=False)