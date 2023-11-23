import uuid

from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class ShowUser(TunedModel):
    id: uuid.UUID
    name: str
    phone: PhoneNumber
    is_verified: bool


class CreateUser(TunedModel):
    name: str
    phone: PhoneNumber
    password: str


class Token(TunedModel):
    access_token: str
    token_type: str
