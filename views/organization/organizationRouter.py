import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import async_session, get_db
from db.dals.organizationdal import OrganizationDAL
from db.models import Owners
from db.models.organizations import Organizations
from views.auth_owner.login import get_current_owner_from_token
from views.organization.schemas import CreateOrganization, ShowOrganization

organization_router = APIRouter()


async def _add_document(file: UploadFile,
                        inn: str,
                        owner_id: uuid.UUID,
                        db: AsyncSession,
                        document_title: str = None):
    async with db as session:
        async with session.begin():
            organization_dal = OrganizationDAL(session)
            return await organization_dal.load_files(file, inn, owner_id, document_title)


async def _delete_worker(inn: str, worker_id: uuid.UUID, owner_id: uuid.UUID, db: AsyncSession):
    async with db as session:
        async with session.begin():
            organization_dal = OrganizationDAL(session)
            return await organization_dal.delete_worker(inn, worker_id, owner_id)


async def _change_worker_image(file: UploadFile, inn: str, worker_id: uuid.UUID, owner_id: uuid.UUID, db: AsyncSession):
    async with db as session:
        async with db.begin():
            organization_dal = OrganizationDAL(session)
            return await organization_dal.change_worker_image(file, inn, worker_id, owner_id)


async def _add_worker(inn: str, post: str, owner_id: uuid.UUID, full_name: str, db: AsyncSession):
    async with db as session:
        async with session.begin():
            organization_dal = OrganizationDAL(session)
            return await organization_dal.create_worker(inn, owner_id, post, full_name)


async def _change_organization_logo(file: UploadFile, inn: str, owner_id: uuid.UUID, db: AsyncSession):
    async with db as session:
        async with session.begin():
            organization_dal = OrganizationDAL(session)
            return await organization_dal.change_organization_logo(file, inn, owner_id)


async def _search_organization_by_id(inn: str, title: str, lim: int, offset: int, db: AsyncSession):
    async with db as session:
        async with session.begin():
            organization_dal = OrganizationDAL(session)
            return await organization_dal.search_organization(inn, title, lim, offset)


async def _show_organization(inn: str, db: AsyncSession):
    async with db as session:
        async with session.begin():
            organization_dal = OrganizationDAL(session)
            return await organization_dal.show_organization(inn)


async def _create_organization(body: CreateOrganization, current_owner, db: AsyncSession):
    async with db as session:
        async with session.begin():
            organization_dal = OrganizationDAL(session)
            organization = await organization_dal.create_organization(
                owner_id=current_owner.id,
                title=body.title,
                address=body.address,
                inn=body.inn,
                ogrn=body.ogrn
            )

            return {
                'response:': 'successfull'}


async def _delete_organization(inn: str, db: AsyncSession, current_owner):
    async with db as session:
        async with session.begin():
            organization_dal = OrganizationDAL(session)
            return await organization_dal.delete_organization(inn, current_owner.id)


async def _show_all_owners_organizations(
        lim: int, offset: int,
        db: AsyncSession,
        current_owner
):
    async with db as session:
        async with session.begin():
            organization_dal = OrganizationDAL(session)
            return await organization_dal.show_all_owners_organizations(lim, offset, current_owner.id)


@organization_router.post('/organization')
async def create_organization(
        body: CreateOrganization,
        current_owner: Owners = Depends(get_current_owner_from_token),
        db: AsyncSession = Depends(get_db)):
    return await _create_organization(body, current_owner, db=db)


@organization_router.get('/search_org')
async def search_org(inn: str = None, title: str = None, lim: int = 5, offset: int = 0,
                     db: AsyncSession = Depends(get_db)):
    return await _search_organization_by_id(inn=inn, title=title, lim=lim, offset=offset, db=db)


@organization_router.get('/organization={inn}')
async def show_organization(inn, db: AsyncSession = Depends(get_db)):
    return await _show_organization(inn=inn, db=db)


@organization_router.delete('/organization={inn}/del')
async def delete_organization(inn: str, db: AsyncSession = Depends(get_db),
                              current_owner: Owners = Depends(get_current_owner_from_token)):
    return await _delete_organization(inn=inn, db=db, current_owner=current_owner)


@organization_router.get('/my-organizations')
async def show_all_owners_organizations(
        lim: int = 5, offset: int = 0,
        db: AsyncSession = Depends(get_db),
        current_owner: Owners = Depends(get_current_owner_from_token)):
    return await _show_all_owners_organizations(lim=lim, offset=offset, db=db, current_owner=current_owner)


@organization_router.put('/organization={inn}/profile/change-logo')
async def change_org_logo(inn: str, file: UploadFile = File(...),
                          current_owner: Owners = Depends(get_current_owner_from_token),
                          db: AsyncSession = Depends(get_db)):
    return await _change_organization_logo(inn=inn, file=file, owner_id=current_owner.id, db=db)


@organization_router.post('/organization={inn}/workers')
async def add_worker(
        inn: str,
        post: str,
        full_name: str,
        db: AsyncSession = Depends(get_db),
        current_owner: Owners = Depends(get_current_owner_from_token)):
    return await _add_worker(inn=inn, post=post, owner_id=current_owner.id, full_name=full_name, db=db)


@organization_router.put('/organization={inn}/worker={worker_id}')
async def change_worker_image(
        worker_id: uuid.UUID,
        inn: str,
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
        current_user: Owners = Depends(get_current_owner_from_token)):
    return await _change_worker_image(file=file, inn=inn, db=db, worker_id=worker_id, owner_id=current_user.id)


@organization_router.delete('/organization={inn}/worker={worker_id}')
async def delete_worker(inn: str,
                        worker_id: uuid.UUID,
                        current_owner: Owners = Depends(get_current_owner_from_token),
                        db: AsyncSession = Depends(get_db)):
    return await _delete_worker(inn=inn, worker_id=worker_id, owner_id=current_owner.id, db=db)


@organization_router.post('/organization={inn}/add-docs')
async def add_documents(inn: str,
                        document_title: str = None,
                        db: AsyncSession = Depends(get_db),
                        file: UploadFile = File(...),
                        current_owner: Owners = Depends(get_current_owner_from_token)
                        ):
    return await _add_document(inn=inn, document_title=document_title, db=db, file=file, owner_id=current_owner.id)
