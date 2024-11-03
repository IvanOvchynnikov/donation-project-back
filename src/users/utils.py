import logging
import uuid
from typing import Any

import jwt
from datetime import timedelta, datetime

from passlib.context import CryptContext

from src.config import Config

passwd_context = CryptContext(
    schemes=["bcrypt"],
)

ACCESS_TOKEN_EXPIRE = 1e9


def generate_password_hash(password: str) -> str:
    return passwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return passwd_context.verify(plain_password, hashed_password)


def create_access_token(user_data: dict, expire: timedelta = timedelta(seconds=ACCESS_TOKEN_EXPIRE)) -> str:
    payload = {'user': user_data,
               'exp': datetime.now() + expire,
               'jti': str(uuid.uuid4()),
               }

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM,
    )
    return token


def decode_token(token: str) -> Any | None:
    try:
        token_data = jwt.decode(token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
