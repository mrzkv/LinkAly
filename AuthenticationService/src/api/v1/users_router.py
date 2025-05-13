from typing import Annotated

from authx import RequestToken
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.db_helper import db_helper
from src.dependencies.token_depends import get_refresh_token
from src.schemas.user import JWKSResponse, TokenResponse, UserCreate, UserLogin
from src.services.user_service import UserService

router = APIRouter(
    prefix=settings.api.v1.root,
    tags=["Users manager"],
)

async def get_service(
        session: Annotated[AsyncSession, Depends(db_helper.get_async_session)],
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

@router.post("/login")
async def login(
        user: UserLogin,
        service: Annotated[UserService, Depends(get_service)],
) -> TokenResponse:
    return await service.login_user(user)

@router.get("/refresh")
async def refresh(
        service: Annotated[UserService, Depends(get_service)],
        refresh_token: Annotated[RequestToken | None, Depends(get_refresh_token)],
) -> TokenResponse:
    return await service.refresh_user_token(refresh_token)

@router.get("/jwks")
async def json_web_key_set() -> JWKSResponse:
    return JWKSResponse(public_key=settings.jwt.JWT_PUBLIC_KEY)
