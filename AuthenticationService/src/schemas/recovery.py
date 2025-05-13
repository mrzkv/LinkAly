from pydantic import BaseModel, EmailStr


class EmailSetRequest(BaseModel):
    email: EmailStr

class PasswordChangeRequest(BaseModel):
    new_password: str
    old_password: str

class EmailSetResponse(BaseModel):
    message: str | None = "check your email"

class NewEmailResponse(BaseModel):
    email: EmailStr

class NewPasswordResponse(BaseModel):
    message: str | None = "your password has been changed"

class ForgotPasswordResponse(BaseModel):
    message: str | None = "check your email"
