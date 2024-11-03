import uuid
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Integer
from sqlmodel import SQLModel, Field, Column


class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    email: str
    nickname: str
    password_hash: str
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.utcnow(),
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.utcnow(),
        ))

    def __repr__(self) -> str:
        return f"<User {self.nickname}>"


class Donation(SQLModel, table=True):
    __tablename__ = "donations"
    id: int = Field(
        sa_column=Column(
            Integer,
            primary_key=True,
            autoincrement=True,
        )
    )
    title: str
    tag: str
    description: str
    image: str  # store images as URLs

    bank_account_number: str
    bank_beneficiary_name: str
    bank_ifsc_code: str

    upi_mobile_number: str
    upi_id: str
