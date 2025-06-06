from sqlalchemy import Column, Index
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR

from src.tables.base import Base


class UrlPair(Base):
    """
    We store short URL variants in the database.
    >>> https://google.com/
    'google.com/'
    >>> https://example.com/profile/mrzkv
    'example.com/profile/mrzkv'

    """
    id = Column(INTEGER, primary_key=True)
    short_url = Column(VARCHAR(30), nullable=False)
    real_url = Column(VARCHAR(512), nullable=False)
    creator_id = Column(INTEGER, nullable=False)
    __table_args__ = (
        Index("ix_url_pairs_short_url", "short_url", postgresql_using="hash"),
    )
