from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Optional


from db.models.users import Users
from db.models.admins import Admins
from uuid import UUID
from pydantic import EmailStr


class AdminDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_admin(
        self,
        org_id: UUID,
        user_id: UUID,
        email: EmailStr,
        social_networks: str,
    ) -> Admins:
        new_admin = Admins(
            org_id=org_id,
            user_id=user_id,
            email=email,
            social_networks=social_networks,
        )
        self.db_session.add(new_admin)
        await self.db_session.flush()
        return new_admin

    async def get_admin_by_phone(self, phone: str) -> Optional[Admins]:
        query = select(Admins).filter(Admins.user.phone == phone)
        res = await self.db_session.execute(query)
        admin_row = res.fetchone()
        if admin_row:
            return admin_row[0]
