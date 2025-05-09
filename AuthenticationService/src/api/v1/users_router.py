from typing import Annotated

from authx import RequestToken
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import JWKSResponse
from src.core.config import settings
from src.core.db_helper import db_helper
from src.schemas.user import TokenResponse, UserCreate, UserLogin
from src.services.user_service import UserService

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Users manager"],
)


async def get_service(
        session: AsyncSession = Depends(db_helper.get_async_session),
) -> UserService:
    return UserService(session)

async def get_refresh_token(
        x_refresh_token: Annotated[str | None, Header(alias="x-refresh-token")],
) -> RequestToken:
    if not x_refresh_token:
        raise HTTPException(status_code=401,
                            detail="Refresh token is required")
    return RequestToken(
        token=x_refresh_token,
        type="refresh",
        location=settings.jwt.JWT_TOKEN_LOCATION[0],
    )

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
