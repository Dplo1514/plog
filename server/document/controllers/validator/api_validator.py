from server.common.exception import AppException
from server.document.controllers.request.dto.dto import UploadFileDTO
from server.document.status import DocumentErrorStatus


def validate_upload_request(request_dto: UploadFileDTO) -> None:
    if not request_dto.file_name or not request_dto.file_size:
        raise AppException(
            status=DocumentErrorStatus.EMPTY_FILE_UPLOADED
        )