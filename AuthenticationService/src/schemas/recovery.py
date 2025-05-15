from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator

from src.utils.password_validator import check_password_vulnerability


class EmailSetRequest(BaseModel):
    email: EmailStr

class PasswordChangeRequest(BaseModel):
    new_password: str
    old_password: str

    @field_validator("new_password", "old_password")
    def validate_password(cls, new: str, old: str) -> str:
        if new == old:
            raise HTTPException(
                status_code=400,
                detail="New password and old password do not match",
            )
        try:
            return check_password_vulnerability(new)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

class EmailSetResponse(BaseModel):
    message: str | None = "check your email"

class NewEmailResponse(BaseModel):
    email: EmailStr

class NewPasswordResponse(BaseModel):
    message: str | None = "your password has been changed"

class ForgotPasswordResponse(BaseModel):
    message: str | None = "check your email"
