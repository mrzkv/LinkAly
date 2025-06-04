from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.core.config import settings
from src.dependencies.services_depends import get_users_service
from src.dependencies.token_depends import get_access_token, get_refresh_token
from src.schemas.user import (
    JWKSResponse,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserMe,
)
from src.security.jwt import TokenPayload
from src.services.user_service import UserService

router = APIRouter(
    prefix=settings.api.v1.root,
    tags=["Users manager"],
)


@router.post(
    path="/register",
    name="Register user",
)
async def register(
        user: UserCreate,
        service: Annotated[
            UserService,
            Depends(get_users_service),
        ],
) -> TokenResponse:
    try:
        return await service.register_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    path="/login",
    name="Login user",
)
async def login(
        user: UserLogin,
        service: Annotated[
            UserService,
            Depends(get_users_service),
        ],
) -> TokenResponse:
    return await service.login_user(user)

@router.get(
    path="/refresh",
    name="refresh access token",
    description="Refreshes access token by refresh token",
    response_model_exclude_none=True,
)
async def refresh(
        refresh_token: Annotated[
            TokenPayload,
            Depends(get_refresh_token),
        ],
        service: Annotated[
            UserService,
            Depends(get_users_service),
        ],
) -> TokenResponse:
    return await service.refresh_user_token(refresh_token)


@router.get(
    path="/jwks",
    name="Json web key set",
    description="Returns RSA256 public key",
)
async def json_web_key_set() -> JWKSResponse:
    return JWKSResponse(public_key=settings.jwt.JWT_PUBLIC_KEY)


@router.get(
    path="/me",
    description="Returns user data -> id, login, email",
    response_model_exclude_none=True,
)
async def me(
        access_token: Annotated[
            TokenPayload,
            Depends(get_access_token),
        ],
        service: Annotated[
            UserService,
            Depends(get_users_service),
        ],
) -> UserMe:
    return await service.get_user_profile(access_token)
