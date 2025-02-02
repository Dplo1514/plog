from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, func

Base = declarative_base()


class TimestampMixin:
    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
        comment="생성일"
    )

    modified_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False, comment="수정일"
    )
