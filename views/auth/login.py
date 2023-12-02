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

from db.dals.userdal import Users
from db.base import get_db
from views.secur.hashing import Hasher
from views.secur.security import create_access_token
from views.auth.schemas import Token
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from other.user_other import get_user_by_phone as get_user_by_phone_for_auth
from other.password_other import get_password_by_password_id as get_password_by_password_id_for_auth


user_login_router = APIRouter()


async def authenticate_user(phone: str, password: str, db: AsyncSession) -> Optional[Users]:
    user = await get_user_by_phone_for_auth(phone=phone, db=db)
    user_password = await get_password_by_password_id_for_auth(user.password_id, db=db)
    if not user or not Hasher.verify_password(password, user_password.password):
        return
    return user

oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl='v1/user/auth/token')


@user_login_router.post('/token', response_model=Token, tags=['user'])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.phone, 'other_custom_data': [1, 2, 3, 4]},
        live_time=access_token_expires,
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme_user), db: AsyncSession = Depends(get_db)
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
        print('username extracted is ', phone)
        if not phone:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_phone_for_auth(phone=phone, db=db)
    if not user:
        raise credentials_exception
    return user


@user_login_router.get("/about_me", tags=['user'])
async def about_me(
    current_user: Users = Depends(get_current_user_from_token),
):
    return {"Success": True, "current_user":
            {
                current_user.name, current_user.phone,
                current_user.id, current_user.is_verified
                }
            }
