from typing import Optional
from fastapi import APIRouter
from fastapi import Depends
from db.base import get_db, async_session
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from db.dals.ownerdal import Owners
from db.models.users import Users
from views.auth_owner.login import get_current_owner_from_token
from shemas import CreatAdmin
from other.user_other import get_user_by_phone
from db.dals.admindal import AdminDAL
from views.owner.shemas import CreatAdmin, ShowAdmin

owner_admins_router = APIRouter()


async def _create_new_admin(body: CreatAdmin, owner: Owners, user: Users) -> ShowAdmin:
    async with async_session() as session:
        async with session.begin():
            admin_dal = AdminDAL
            new_admin = await admin_dal.create_admin(
                email=body.email, social_networks=body.social_networks,
                user_id=user.id, org_id=owner
            )


@owner_admins_router.post('add_admin', tags=['owner'])
async def add_admin(
        owner: Owners = Depends(get_current_owner_from_token),
        body: CreatAdmin = Depends(),
        db: AsyncSession = Depends(get_db)
):
    user = get_user_by_phone(body.phone, db)