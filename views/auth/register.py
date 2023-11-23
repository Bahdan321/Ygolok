from fastapi import APIRouter
from views.auth.schemas import CreateUser, ShowUser
from db.base import async_session
from db.dals.userdal import UserDAL
from db.dals.passworddal import PasswordDAL
from views.secur.hashing import Hasher
from views.secur.change_number import format_phone_number

user_register_router = APIRouter()


async def _create_new_user(body: CreateUser) -> ShowUser:
    async with async_session() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            password_dal = PasswordDAL(session)
            password = await password_dal.create_password(hashed_password=Hasher.get_password_hash(body.password))
            user = await user_dal.create_user(
                name=body.name, phone=body.phone,
                password_id=password.id
            )
            return ShowUser(
                id=user.id, name=user.name, phone=format_phone_number(user.phone), is_verified=user.is_verified
            )


@user_register_router.post('/', response_model=ShowUser, tags=['user'])
async def register(body: CreateUser) -> ShowUser:
    return await _create_new_user(body)
