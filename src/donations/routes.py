from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from .schemas import DonationResponseModel
from .service import DonationService
from ..users.dependencies import AccessTokenBearer

donations_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@donations_router.get("/donations/{donation_id}", response_model=DonationResponseModel)
async def get_donation(
        donation_id: int,
        session: AsyncSession = Depends(get_session),
        user_details=Depends(access_token_bearer)
):
    donation = await DonationService.get_donation_by_id(donation_id, session)
    if not donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")
    return donation
