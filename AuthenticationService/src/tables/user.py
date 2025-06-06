from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import (
    BIGINT,
    VARCHAR,
)

from src.tables.base import Base


class User(Base):
    id = Column(BIGINT, primary_key=True, index=True)
    login = Column(VARCHAR(255), unique=True, nullable=False)
    email = Column(VARCHAR(255), unique=True, nullable=True)
    hashed_password = Column(VARCHAR(512), nullable=False)

