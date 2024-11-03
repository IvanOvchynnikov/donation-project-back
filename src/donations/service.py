from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Donation


class DonationService:
    @staticmethod
    async def get_donation_by_id(donation_id: int, session: AsyncSession):
        statement = select(Donation).where(Donation.id == donation_id)
        result = await session.exec(statement)
        return result.first()
