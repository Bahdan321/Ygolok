from db.dals.userdal import UserDAL
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_by_phone(phone: str, db: AsyncSession):
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            return await user_dal.get_user_by_phone(phone)
