import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class User(BaseModel):
    uid: uuid.UUID
    nickname: str
    password_hash: str = Field(exclude=True)
    email: str
    created_at: datetime
    updated_at: datetime


class UserCreateModel(BaseModel):
    nickname: str
    email: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "nickname": "johndoe",
                "email": "johndoe123@co.com",
                "password": "testpass123",
            }
        }
    }


class UserLoginModel(BaseModel):
    nickname: str
    password: str
