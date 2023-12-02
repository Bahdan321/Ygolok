import uuid
from fastapi import File, UploadFile
from pydantic import BaseModel


class CreateOrganization(BaseModel):
    title: str
    address: str
    inn: str
    ogrn: str


class ShowOrganization(BaseModel):
    owner_name: str
    address: str
    org_title: str
    org_logo_url: str
    inn: str
    ogrn: str


