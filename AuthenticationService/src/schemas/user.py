import re
from typing import Annotated

from fastapi import HTTPException
from pydantic import BaseModel, field_validator


class UserCreate(BaseModel):
    login: str
    password: str

    @field_validator("password")
    def validate_password(cls,
                          password: str,
    ) -> Annotated[str | HTTPException, "password validator"]:
        if len(password) < 8:
            raise HTTPException(status_code=400,
                                detail="Password must be at"
                                       " least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise HTTPException(status_code=400,
                                detail="Password must contain at"
                                       " least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise HTTPException(status_code=400,
                                detail="Password must contain at"
                                       " least one lowercase letter")
        if not re.search(r"\d", password):
            raise HTTPException(status_code=400,
                                detail="Password must contain at"
                                       " least one digit")
        if not re.search(r'[!@#$%^&*(),.?"\':{}|<>/\\]', password):
            raise HTTPException(status_code=400,
                                detail="Password must contain at"
                                       " least one special character")

        return password


class UserLogin(BaseModel):
    password: str
    login: str

class TokenResponse(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str

class JWKSResponse(BaseModel):
    public_key: str

class SerializedUser(BaseModel):
    login: str
    hashed_password: str

