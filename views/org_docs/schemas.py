import uuid

from pydantic import BaseModel


class OrgDoc(BaseModel):
    id: uuid.UUID
    doc_title: str
    address: str
    documet: str
    