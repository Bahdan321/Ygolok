import uuid

from views.auth.schemas import TunedModel
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import EmailStr


# TODO разобраться с валидацией на соц сеть: придумать что это будет
#  ссылка или никнейм, если сылка то от чего вк, телега может ватсап в общем
#  подумать над этим

class CreatAdmin(TunedModel):
    phone: PhoneNumber
    email: EmailStr
    social_networks: str


class ShowAdmin(TunedModel):
    id: uuid.UUID
    name: str
    phone: PhoneNumber
    is_verified: bool
