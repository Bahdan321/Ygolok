import uuid
from datetime import datetime
from pydantic import BaseModel


class ShowFeedback(BaseModel):
    id: uuid.UUID
    user_name: str
    body: str
    created_at: datetime


class CreateFeedback(BaseModel):
    body: str
    inn: str

