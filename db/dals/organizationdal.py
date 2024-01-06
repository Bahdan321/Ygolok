import uuid

import sqlalchemy
from fastapi import HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from typing import Optional

from db.models.organizationdocuments import OrganizationDocument
from config import DEFAULT_PATH_ORG_IMAGE, DEFAULT_PATH_WORKER_IMAGE
from db.models import Workers
from db.models.organizations import Organizations
from views.organization.schemas import ShowOrganization
from views.organization.utils import upload_photos, upload_files, validate_organization_inn


class OrganizationDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_organization(
            self,
            owner_id: uuid.UUID, title: str,
            address: str, inn: str,
            ogrn: str
    ) -> Organizations:
        validate_organization_inn(inn)
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
                Organizations.logo).where(Organizations.inn.ilike(f"%{inn}%")).limit(lim).offset(offset)

            res = await self.db_session.execute(query)
            organization_row = [r._asdict() for r in res.fetchall()]

        elif title:
            query = select(
                Organizations.title,
                Organizations.inn,
                Organizations.address,
                Organizations.logo).where(Organizations.title.ilike(f"%{title}%")).limit(lim).offset(offset)

            res = await self.db_session.execute(query)
            organization_row = [r._asdict() for r in res.fetchall()]

        if organization_row:
            return {'response: ': organization_row}

        return {'response:': 'org not found'}

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
        query = select(Organizations).where(Organizations.inn == inn, owner_id == Organizations.owner_id)
        res = await self.db_session.execute(query)
        org_row = res.fetchone()

        if not org_row:

            raise HTTPException(status_code=404, detail='org not found')

        stmt = update(Organizations).where(Organizations.inn == inn, Organizations.owner_id == owner_id).values(logo=upload_photos(file, inn=inn, image_path="static/orgLogos/"))

        await self.db_session.execute(stmt)
        await self.db_session.commit()

        return {'response: ': 'successful'}

    async def create_worker(self, inn: str, owner_id: uuid.UUID, post: str, full_name: str):
        query = select(Organizations.id).where(inn == Organizations.inn, owner_id == Organizations.owner_id)
        res = await self.db_session.execute(query)
        organization_id = res.fetchone()

        if not organization_id:
            raise HTTPException(status_code=404, detail='org not found')

        new_worker = Workers(
            org_id=organization_id[0],
            full_name=full_name,
            post=post,
            avatar=DEFAULT_PATH_WORKER_IMAGE
        )

        self.db_session.add(new_worker)
        await self.db_session.flush()

        return {'response:': 'successful'}

    async def change_worker_image(self, file: UploadFile, inn: str, worker_id: uuid.UUID, owner_id: uuid.UUID):
        query = select(Organizations.id).where(inn == Organizations.inn, owner_id == Organizations.owner_id)
        res = await self.db_session.execute(query)
        organization_id = res.fetchone()

        if not organization_id:
            raise HTTPException(status_code=404, detail='org not found')

        query = select(Workers).where(Workers.org_id == organization_id[0], worker_id == Workers.id)
        res = await self.db_session.execute(query)
        worker = res.fetchone()

        if not worker:
            raise HTTPException(status_code=404, detail='worker not found')

        stmt = update(Workers).where(worker_id == Workers.id).values(avatar=upload_photos(file=file, worker_id=worker_id, image_path="static/workerLogo/"))
        await self.db_session.execute(stmt)
        await self.db_session.commit()

        return {'response:': 'successful'}

    async def delete_worker(self, inn: str, worker_id: uuid.UUID, owner_id: uuid.UUID):

        query = select(Organizations.id).where(inn == Organizations.inn, owner_id == Organizations.owner_id)
        res = await self.db_session.execute(query)
        organization_id = res.fetchone()

        if not organization_id:
            raise HTTPException(status_code=404, detail='org not found')

        query = select(Workers).where(Workers.org_id == organization_id[0], worker_id == Workers.id)
        res = await self.db_session.execute(query)
        worker = res.fetchone()

        if not worker:
            raise HTTPException(status_code=404, detail='worker not found')

        stmt = delete(Workers).where(Workers.org_id == organization_id[0], worker_id == Workers.id)
        await self.db_session.execute(stmt)
        await self.db_session.commit()

        return {'response: ': 'successful'}

    async def load_files(self, file: UploadFile, inn: str, owner_id: uuid.UUID, document_title: str = None):
        query = select(Organizations.id).where(inn == Organizations.inn, Organizations.owner_id == owner_id)
        res = await self.db_session.execute(query)
        organization_id = res.fetchone()
        content_type = file.content_type

        if not organization_id:
            raise HTTPException(status_code=404, detail='org not found')

        if not document_title:
            document_title = file.filename

        # documemt ---- не знаю что это за поле (возможно его надо удалить)
        new_organization_document = OrganizationDocument(
            org_id=organization_id[0],
            doc_title=document_title,
            address=upload_files(file=file, inn=inn),
            document="Nothing"
        )

        self.db_session.add(new_organization_document)
        await self.db_session.flush()

        return {"response": 'successful'}


