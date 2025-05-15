import re
from typing import Annotated
from fastapi import HTTPException
from pydantic import BaseModel, field_validator

from src.utils.password_validator import check_password_vulnerability

class UserLogin(BaseModel):
    password: str
    login: str

class UserCreate(BaseModel):
    login: str
    password: str

    @field_validator("password")
    def validate_password(
            cls,
            password: str,
    ) -> Annotated[str | HTTPException, "password validator"]:
        try:
            return check_password_vulnerability(password)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))



class TokenResponse(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str

class JWKSResponse(BaseModel):
    public_key: str

class SerializedUser(BaseModel):
    login: str
    hashed_password: str

