from urllib.parse import urlparse

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator


class SerializedUrlPair(BaseModel):
    short_url: str = Field(max_length=30)
    real_url: str
    creator_id: int

    @field_validator("real_url", mode="before")
    def validate_real_url(cls, real_url: str) -> str:
        url = real_url.strip()
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc or not parsed.hostname:
            raise HTTPException(status_code=400, detail="Invalid URL format")
        return url[len(parsed.scheme) + 3:]


class NewUrlPair(BaseModel):
    short_url: str = Field(max_length=30)
    real_url: str

    @field_validator("short_url")
    def validate_short_url(cls, short_url: str) -> str:
        if not short_url.isalnum():
            raise ValueError("short_url must be alphanumeric")
        return short_url

class SuccessCreateUrlPair(SerializedUrlPair):
    url_id: int

class UserUrlPair(BaseModel):
    id: int
    short_url: str
    real_url: str
