import uuid
import re
from typing import Optional

from pydantic import BaseModel
from pydantic.v1 import validator
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

    # TODO найти рабочий способ проверки валидности номера отличный от PhoneNumber
    # @validator("phone")
    # def phone_validation(cls, v):
    #
    #     regex = r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
    #     if v and not re.search(regex, v, re.I):
    #         raise ValueError("Phone Number Invalid.")
    #     return v

    class Config:
        orm_mode = True
        use_enum_values = True


class Token(TunedModel):
    access_token: str
    token_type: str
