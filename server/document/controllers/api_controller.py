from flask import Blueprint, request
from sqlalchemy import text

from server.common.database import make_session
from server.common.response import Response
from server.document.controllers.request.vo.factory import \
    upload_file_vo_factory
from server.document.controllers.request.vo.vo import UploadFileVo
from server.document.controllers.request.dto.dto import UploadFileDTO
from server.document.controllers.validator.api_validator import \
    validate_upload_request
from server.document.models import Document
from server.document.service.api_service import handle_upload

router: Blueprint = Blueprint(
    'documents_api',
    __name__,
    url_prefix='/api/documents'
)


@router.route("/upload", methods=["POST"])
def upload_chunk() -> dict:
    request_dto: UploadFileDTO = UploadFileDTO(
        file_name=request.form.get("file_name", ""),
        chunk_size=int(request.form.get("chunk_size", 0)),
        file_size=int(request.form.get("file_size", 0)),
    )
    validate_upload_request(request_dto)
    vo: UploadFileVo = upload_file_vo_factory(request_dto)
    return handle_upload(vo)


@router.route("/list", methods=["GET"])
def get_documents() -> dict:
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        search_query = request.args.get("q", "").strip()

        session = make_session()
        query = session.query(Document)

        if search_query:
            query = query.filter(
                text("to_tsvector('simple', name) @@ to_tsquery(:q)")).params(
                q=search_query)

        total_count = query.count()
        documents = query.offset((page - 1) * per_page).limit(per_page).all()
        data = {
            "total": total_count,
            "page": page,
            "per_page": per_page,
            "data": [
                {
                    "id": str(doc.id),
                    "name": doc.name,
                    "path": doc.path,
                    "status": doc.status.value,
                    "created_at": doc.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "modified_at": doc.modified_at.strftime("%Y-%m-%d %H:%M:%S")
                }
                for doc in documents
            ]
        }

        return Response(
            code=200,
            message="ss",
            data=data
        ).model_dump()

    finally:
        session.close()
