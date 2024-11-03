from datetime import timedelta

from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from fastapi import status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.responses import JSONResponse

from src.db.main import get_session
from src.users.schemas import User, UserCreateModel, UserLoginModel
from src.users.service import UserService
from .dependencies import AccessTokenBearer
from .utils import create_access_token, verify_password

users_router = APIRouter()
users_service = UserService()
access_token_bearer = AccessTokenBearer()
REFRESH_TOKEN_EXPIRY = 7  # in days


@users_router.get('/user/{nickname}', response_model=User)
async def get_user(nickname: str,
                   session: AsyncSession = Depends(get_session),
                   user_details=Depends(access_token_bearer)):
    user = await users_service.get_user_by_nickname(nickname=nickname, session=session)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@users_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    user_exists = await users_service.user_exists(nickname=user_data.nickname, session=session)

    if user_exists:
        raise HTTPException(status_code=400, detail='User already exists.')

    new_user = await users_service.create_user(user_data, session=session)

    return {
        "message": "Account Created! Check email to verify your account",
        "user": new_user,
    }


@users_router.post('/login')
async def login(user_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    nickname = user_data.nickname
    password = user_data.password

    user = await users_service.get_user_by_nickname(nickname=nickname, session=session)
    if user:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data={
                    'nickname': user.nickname,
                    'user_uid': str(user.uid),
                },
            )
            return JSONResponse(
                content={
                    'message': 'Login Successful!',
                    'access_token': access_token,
                    'user': {
                        'nickname': user.nickname,
                        'user_uid': str(user.uid),
                    }
                }
            )
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
