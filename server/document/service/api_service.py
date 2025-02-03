import logging
import os
import uuid
from typing import Generator

from flask import request, stream_with_context

from server.common.database import make_session
from server.document.models.document import Document, DocumentStatus

UPLOAD_FOLDER = "document"


def handle_upload(filename: str, total_size: int, chunk_size: int):
    """
    파일을 chunk 단위로 저장하면서 진행률을 반환.
    업로드 도중 오류가 발생하면 미완성 파일을 삭제함.

    :param filename: 업로드할 파일명
    :param total_size: 파일의 전체 크기 (바이트 단위)
    :param chunk_size: 업로드할 chunk 크기 (바이트 단위)
    :return: Flask Response (Server-Sent Events)
    """
    file_uuid: str = str(uuid.uuid4())
    file_path: str = os.path.join(UPLOAD_FOLDER, filename)

    chunks = _save_file_chunks(
        file_path,
        chunk_size,
        total_size,
        filename,
        file_uuid
    )
    return stream_with_context(chunks)


def _save_file_chunks(
    _file_path: str,
    _chunk_size: int,
    _total_size: int,
    _filename: str,
    _file_uuid: str
) -> Generator[str, None, None]:
    """
    Chunk 데이터를 받아 파일을 저장하며 진행률을 반환.
    파일 저장이 완료되면 DB에 저장.
    오류 발생 시 파일 삭제.

    :param _file_path: 저장할 파일의 경로
    :param _chunk_size: 업로드할 단위 크기 (바이트 단위)
    :param _total_size: 파일의 전체 크기 (바이트 단위)
    :param _filename: 파일 이름
    :param _file_uuid: UUID 기반 파일 ID
    :return: SSE (Server-Sent Events) 형식의 진행률 데이터
    """
    uploaded_size: int = os.path.getsize(_file_path) \
        if os.path.exists(_file_path) \
        else 0

    try:
        with open(_file_path, "ab") as f:
            while True:
                chunk: bytes = request.stream.read(_chunk_size)
                if not chunk:
                    _save_document_to_db(_file_uuid, _filename, _file_path)
                    break

                f.write(chunk)
                uploaded_size += len(chunk)
                progress: int = int((uploaded_size / _total_size) * 100)

                yield f"data: {progress}\n\n"

    except Exception:
        if os.path.exists(_file_path):
            os.remove(_file_path)
        yield f"data: 0\n\n"


def _save_document_to_db(file_uuid: str, filename: str, file_path: str):
    """
    파일이 성공적으로 업로드된 경우 DB에 저장.

    :param file_uuid: UUID 기반 파일 ID
    :param filename: 저장된 파일명
    :param file_path: 저장된 파일의 경로
    """

    try:
        document = Document(
            id=file_uuid,
            name=filename,
            path=file_path,
            status=DocumentStatus.INIT
        )
        session = make_session()
        session.add(document)
        session.commit()
    except Exception as e:
        logging.info(f"Error saving document to DB: {e}")
        session.rollback()
    finally:
        session.close()
