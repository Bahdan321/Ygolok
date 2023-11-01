from sqlalchemy import UUID, ForeignKey, String, Boolean, Column
from database import Base
from models.owners import Owners

class Organizations(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID,ForeignKey("Owners.id"),nullable=False)
    title = Column(String,nullable=False)
    address = Column(String,nullable=False)
    name = Column(String,nullable=False)
    logo = Column(String,nullable=False)
    inn = Column(String,nullable=False)
    ogrn = Column(String,nullable=False)
 