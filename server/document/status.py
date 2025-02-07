from http import HTTPStatus

from server.common.status import BaseStatus


class DocumentSuccessStatus(BaseStatus):
    http_status: HTTPStatus
    code: int
    message: str

    FILE_UPLOAD_SUCCESS = (
        HTTPStatus.OK,
        3001,
        "Operation Success"
    )


class DocumentErrorStatus(BaseStatus):
    http_status: HTTPStatus
    code: int
    message: str

    FILE_UPLOAD_FAILURE = (
        HTTPStatus.INTERNAL_SERVER_ERROR,
        3101,
        "Internal Server Error"
    )
    EMPTY_FILE_UPLOADED = (
        HTTPStatus.BAD_REQUEST,
        3102,
        "Bad Request"
    )
