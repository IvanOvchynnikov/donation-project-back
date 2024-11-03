from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import User
from .utils import generate_password_hash, verify_password

from .schemas import UserCreateModel


class UserService:
    @staticmethod
    async def get_user_by_nickname(nickname: str, session: AsyncSession):
        statement = select(User).where(User.nickname == nickname)

        result = await session.exec(statement)

        user = result.first()
        if not user:
            user = None

        return user

    async def user_exists(self, nickname, session: AsyncSession):
        user = await self.get_user_by_nickname(nickname, session)

        return True if user is not None else False

    @staticmethod
    async def create_user(user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)

        new_user.password_hash = generate_password_hash(user_data_dict["password"])

        session.add(new_user)

        await session.commit()

        return new_user
