from datetime import timedelta
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from db.dals.ownerdal import OwnerDAL, Owners
from db.base import get_db
from db.dals.passworddal import PasswordDAL
from views.secur.hashing import Hasher
from views.secur.security import create_access_token
from views.auth_owner.schemas import Token
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# from views.auth.login import _get_password_by_password_id_for_auth

owner_login_router = APIRouter()


async def _get_password_by_password_id_for_auth(password_id: str, db: AsyncSession):
    async with db as session:
        async with session.begin():
            password_dal = PasswordDAL(session)
            return await password_dal.get_password(password_id)


async def _get_owner_by_phone_for_auth(phone: str, db: AsyncSession) -> Optional[Owners]:
    async with db as session:
        async with session.begin():
            owner_dal = OwnerDAL(session)
            return await owner_dal.get_owner_by_phone(phone)


async def authenticate_owner(phone: str, password: str, db: AsyncSession) -> Optional[Owners]:
    owner = await _get_owner_by_phone_for_auth(phone=phone, db=db)
    owner_password = await _get_password_by_password_id_for_auth(owner.password_id, db=db)
    if not owner or not Hasher.verify_password(password, owner_password.password):
        return
    return owner

oauth2_scheme_owner = OAuth2PasswordBearer(tokenUrl='/v1/owner/auth/token',)


@owner_login_router.post('/token', response_model=Token, tags=['owner'])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    owner = await authenticate_owner(form_data.username, form_data.password, db)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect mobile phone or password',
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': owner.phone, 'other_custom_data': [1, 2, 3, 4]},
        live_time=access_token_expires,
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


async def get_current_owner_from_token(
    token: str = Depends(oauth2_scheme_owner), db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
    )
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        phone: str = payload.get('sub')
        if not phone:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    owner = await _get_owner_by_phone_for_auth(phone=phone, db=db)
    if not owner:
        raise credentials_exception
    return owner


@owner_login_router.get("/about_me", tags=['owner'])
async def about_me(
    current_owner: Owners = Depends(get_current_owner_from_token),
):
    return {"Success": True, "current_user":
            {
                current_owner.name, current_owner.last_name,
                current_owner.patronymic, current_owner.ogrn,
                current_owner.inn,
                current_owner.id, current_owner.is_verified
                }
            }
