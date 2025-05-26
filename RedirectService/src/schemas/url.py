from pydantic import (
    BaseModel,
    Field,
    field_serializer,
    field_validator
)
from src.utils.url_convertor import url_convertor


class SerializedUrlPair(BaseModel):
    short_url: str = Field(max_length=30)
    real_url: str
    creator_id: int

    @field_serializer("real_url")
    def validate_real_url(cls, real_url: str) -> str:
        return url_convertor(real_url)


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
