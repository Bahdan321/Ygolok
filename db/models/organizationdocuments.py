import uuid

from sqlalchemy import UUID, ForeignKey, String, Column
from db.models.base_model import Base


class OrganizationDocument(Base):
    __tablename__ = "organizationdocument"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID, ForeignKey("organizations.id"), nullable=False)
    doc_title = Column(String, nullable=False)
    address = Column(String, nullable=False)
    document = Column(String, nullable=False)

