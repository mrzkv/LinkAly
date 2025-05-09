from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service import UserService
from src.core.config import settings
from src.core.db_helper import db_helper
from src.schemas.user import TokenResponse, UserCreate

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Users manager"],
)
async def get_service(
        session: AsyncSession = Depends(db_helper.get_async_session),
) -> UserService:
    return UserService(session)


@router.post("/register")
async def register(
        user: UserCreate,
        service: Annotated[UserService, Depends(get_service)],
) -> TokenResponse:
    try:
        return await service.register_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

