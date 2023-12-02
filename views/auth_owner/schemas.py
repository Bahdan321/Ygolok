import uuid

from pydantic_extra_types.phone_numbers import PhoneNumber
from views.auth.schemas import TunedModel, Token
from typing import Optional
from pydantic import Field
from typing_extensions import Annotated


class ShowOwner(TunedModel):
    id: uuid.UUID
    name: str
    phone: PhoneNumber
    is_verified: bool
    last_name: str
    inn: str
    ogrn: str
    patronymic: Optional[str]


# TODO таже самая задача по валидации номера, смотреть todo в views/auth/schemas.py
class CreateOwner(TunedModel):
    name: Annotated[str, Field(pattern=r'^([А-Я]{1}[а-яё]{1,23}|[A-Z]{1}[a-z]{1,23})$')]
    phone: PhoneNumber
    password: str
    last_name: str = Field(pattern=r'^([А-Я]{1}[а-яё]{1,30}|[A-Z]{1}[a-z]{1,30})$')
    inn: str
    ogrn: str
    patronymic: Optional[str] = Field(pattern=r'^([А-Я]{1}[а-яё]{1,26}|[A-Z]{1}[a-z]{1,26})$')
