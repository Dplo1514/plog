from enum import Enum
from http import HTTPStatus


class BaseStatus(Enum):
    http_status: HTTPStatus
    code: int
    message: str

    def __new__(cls, http_status, code, message):
        obj = object.__new__(cls)
        obj._value_ = code
        obj.code = code
        obj.message = message
        return obj


class CommonStatus(BaseStatus):
    http_status: HTTPStatus
    code: int
    message: str

    SUCCESS = (
        HTTPStatus.OK,
        200,
        "Operation Success"
    )
    CREATED = (
        HTTPStatus.CREATED,
        201,
        "Operation Success"
    )
    BAD_REQUEST = (
        HTTPStatus.BAD_REQUEST,
        400,
        "Bad Request"
    )
    NOT_FOUND = (
        HTTPStatus.NOT_FOUND,
        404,
        "Not Found"
    )
    INTERNAL_SERVER_ERROR = (
        HTTPStatus.INTERNAL_SERVER_ERROR,
        500,
        "Internal Server Error"
    )
