from pydantic import BaseModel, Field, field_serializer

from src.utils.url_convertor import url_convertor


class SerializedUrlPair(BaseModel):
    short_url: str = Field(max_length=30)
    real_url: str

    @field_serializer("real_url")
    def validate_real_url(cls, real_url: str) -> str:
        return url_convertor(real_url)
