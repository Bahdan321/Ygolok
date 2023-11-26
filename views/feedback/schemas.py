import uuid
from datetime import datetime
from sqlalchemy import TIMESTAMP

from pydantic import BaseModel


class ShowFeedback(BaseModel):
    id: uuid.UUID
    user_name: str
    body: str
    created_at: datetime



