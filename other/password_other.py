from db.dals.passworddal import PasswordDAL
from sqlalchemy.ext.asyncio import AsyncSession


async def get_password_by_password_id(password_id: str, db: AsyncSession):
    async with db as session:
        async with session.begin():
            password_dal = PasswordDAL(session)
            return await password_dal.get_password(password_id)