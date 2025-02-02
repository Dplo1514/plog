import os

from flask import Blueprint, request, jsonify
from sqlalchemy import text

from server.common.database import make_session
from server.common.response import Response
from server.document.models import Document
from server.document.service.api_service import handle_upload

router: Blueprint = Blueprint(
    'documents_api',
    __name__,
    url_prefix='/api/documents'
)


@router.route("/upload", methods=["POST"])
def upload_chunk() -> Response:
    filename: str = request.headers.get("X-File-Name", "")
    total_size: int = int(request.headers.get("X-File-Size", 0))
    chunk_size: int = int(request.headers.get("X-Chunk-Size", 1024 * 1024))

    if not filename or total_size == 0:
        return jsonify({"error": "Invalid request"}), 400

    filename = os.path.basename(filename)
    return handle_upload(filename, total_size, chunk_size)


@router.route("/list", methods=["GET"])
def get_documents():
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
                    "created_at": doc.created_at,
                    "modified_at": doc.modified_at
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
