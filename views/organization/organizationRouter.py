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


async def _change_organization_logo(file: UploadFile, inn: str, owner_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
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
async def search_org_by_inn(inn: str = None, title: str = None, lim: int = 5, offset: int = 0,
                            db: AsyncSession = Depends(get_db)):
    return await _search_organization_by_id(inn=inn, title=title, lim=lim, offset=offset, db=db)


@organization_router.get('/organization/{inn}')
async def show_organization(inn, db: AsyncSession = Depends(get_db)):
    return await _show_organization(inn=inn, db=db)


@organization_router.delete('/organization/del')
async def delete_organization(inn: str, db: AsyncSession = Depends(get_db), current_owner: Owners = Depends(get_current_owner_from_token)):
    return await _delete_organization(inn=inn, db=db, current_owner=current_owner)


@organization_router.get('/my-organizations')
async def show_all_owners_organizations(
        lim: int = 5, offset: int = 0,
        db: AsyncSession = Depends(get_db),
        current_owner: Owners = Depends(get_current_owner_from_token)):

    return await _show_all_owners_organizations(lim=lim, offset=offset, db=db, current_owner=current_owner)


@organization_router.put('/organization/profile/change-logo')
async def change_org_logo(inn: str, file: UploadFile = File(...), current_owner: Owners = Depends(get_current_owner_from_token), db: AsyncSession = Depends(get_db)):
    return await _change_organization_logo(inn=inn, file=file, owner_id=current_owner.id, db=db)
