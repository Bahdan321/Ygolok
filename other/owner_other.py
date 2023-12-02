from db.dals.ownerdal import OwnerDAL, Owners
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional


async def get_owner_by_phone(phone: str, db: AsyncSession) -> Optional[Owners]:
    async with db as session:
        async with session.begin():
            owner_dal = OwnerDAL(session)
            return await owner_dal.get_owner_by_phone(phone)
