import os
import uuid

import sqlalchemy
from fastapi import HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from typing import Optional

from config import DEFAULT_PATH_ORG_IMAGE
from db.models.organizations import Organizations
from views.organization.schemas import ShowOrganization


class OrganizationDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    @staticmethod
    def __upload_photos(file: UploadFile, inn: str):
        content_type = file.content_type
        if content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid file type")

        cwd = os.getcwd()
        path_image_dir = "static/orgLogos/"
        full_image_path = os.path.join(cwd, path_image_dir, file.filename)

        if not os.path.exists(path_image_dir):
            os.mkdir(path_image_dir)

        file_name = f'{path_image_dir}{inn}.png'

        with open(file_name, 'wb+') as f:
            f.write(file.file.read())
            f.flush()
            f.close()

        return file_name

    @staticmethod
    def __validate_organization_inn(inn: str):
        if not inn.isdigit() or len(inn) != 10:
            raise HTTPException(status_code=400, detail="invalid inn")

        coefficients = [2, 4, 10, 3, 5, 9, 4, 6, 8]
        control_sum = sum([int(inn[i]) * coefficients[i] for i in range(9)]) % 11 % 10

        if str(control_sum) != inn[9]:
            raise HTTPException(status_code=400, detail="invalid inn")

        return inn

    async def create_organization(
            self,
            owner_id: uuid.UUID, title: str,
            address: str, inn: str,
            ogrn: str
    ) -> Organizations:
        self.__validate_organization_inn(inn)
        try:

            new_organization = Organizations(
                owner_id=owner_id,
                title=title,
                address=address,
                logo=DEFAULT_PATH_ORG_IMAGE,
                inn=inn,
                ogrn=ogrn
            )

            self.db_session.add(new_organization)
            await self.db_session.flush()
            return new_organization
        except IntegrityError:
            raise HTTPException(status_code=409, detail='inn already exists')

    async def search_organization(self, inn: str, title: str, lim: int, offset: int):
        if lim < 0 or offset < 0:
            return {'response: ': 'value cannot be negative'}

        if inn:
            query = select(
                Organizations.title,
                Organizations.inn,
                Organizations.address,
                Organizations.logo).where(Organizations.inn.like(f'%{inn}%')).limit(lim).offset(offset)

            res = await self.db_session.execute(query)
            organization_row = [r._asdict() for r in res.fetchall()]

        elif title:
            query = select(
                Organizations.title,
                Organizations.inn,
                Organizations.address,
                Organizations.logo).where(Organizations.title.like(f'%{title}%')).limit(lim).offset(offset)

            res = await self.db_session.execute(query)
            organization_row = [r._asdict() for r in res.fetchall()]

        if organization_row:
            return {'response: ': organization_row}

    async def show_organization(self, inn: str):
        query = select(Organizations).where(Organizations.inn == inn)
        res = await self.db_session.execute(query)
        org_row = res.fetchone()

        if org_row:
            return {'response: ': org_row[0]}

        raise HTTPException(status_code=404, detail='Not Found')

    async def delete_organization(self, inn: str, owner_id: uuid.UUID):
        stmt = delete(Organizations).where(Organizations.owner_id == owner_id, Organizations.inn == inn)

        await self.db_session.execute(stmt)
        await self.db_session.commit()

        return {'response: ': 'successful'}

    async def show_all_owners_organizations(self, lim: int, offset: int, owner_id: uuid.UUID):
        if not owner_id:
            raise HTTPException(status_code=401, detail='Unauthorized')

        query = select(Organizations).where(Organizations.owner_id == owner_id).limit(lim).offset(offset)
        res = await self.db_session.execute(query)
        organization_row = [r._asdict() for r in res.fetchall()]

        if organization_row:
            return {'response: ': organization_row}

        raise HTTPException(status_code=404, detail='Not found')

    async def change_organization_logo(self, file: UploadFile, inn: str, owner_id: uuid.UUID):
        query = select(Organizations).where(Organizations.inn == inn)
        res = await self.db_session.execute(query)
        org_row = res.fetchone()

        if not org_row:
            print(1)
            raise HTTPException(status_code=404, detail='org not found')

        stmt = update(Organizations).where(Organizations.inn == inn, Organizations.owner_id == owner_id).values(logo=self.__upload_photos(file, inn))

        await self.db_session.execute(stmt)
        await self.db_session.commit()

        return {'response: ': 'successful'}



