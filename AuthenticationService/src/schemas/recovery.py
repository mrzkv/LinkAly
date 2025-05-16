from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator, model_validator

from src.utils.password_validator import check_password_vulnerability


class EmailSetRequest(BaseModel):
    email: EmailStr

class PasswordChangeRequest(BaseModel):
    new_password: str
    old_password: str

    @model_validator(mode="after")
    def check_password_different(self) -> str:
        if self.new_password == self.old_password:
            raise HTTPException(
                status_code=400,
                detail="The new password and the old password must not match.",
            )
        return self

    @field_validator("new_password")
    def validate_new_password(cls, new_password: str) -> str:
        try:
            return check_password_vulnerability(new_password)
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
