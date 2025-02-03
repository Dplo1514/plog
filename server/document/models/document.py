import uuid
from enum import Enum
from sqlalchemy import Column, Text, Index, text, String
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.sql import func
from server.common.model import TimestampMixin, Base


class DocumentStatus(str, Enum):
    INIT = "INIT"
    CHUNKING = "CHUNKING"
    EMBEDDING = "EMBEDDING"
    INDEXING = "INDEXING"


class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="UUID"
    )
    name = Column(
        String(255),
        nullable=False,
        comment="파일 이름 (한국어 Full Text Search 지원)"
    )
    path = Column(
        String(255),
        nullable=False,
        comment="파일 저장 경로"
    )

    status = Column(
        ENUM(DocumentStatus, name="document_status", create_type=True),
        default=DocumentStatus.INIT,
        nullable=False,
        comment="파일 처리 상태"
    )

    __table_args__ = (
        Index(
            "idx_documents_name",
            text("to_tsvector('simple', name)"),
            postgresql_using="GIN"
        ),
    )
