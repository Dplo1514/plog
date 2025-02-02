from enum import Enum


class BaseStatus(Enum):
    code: int
    message: str

    def __new__(cls, code, message):
        obj = object.__new__(cls)
        obj._value_ = code
        obj.code = code
        obj.message = message
        return obj

class CommonStatus(BaseStatus):
    code: int
    message: str

    SUCCESS = (200, "Success")
    CREATED = (201, "Created")
    BAD_REQUEST = (400, "Bad Request")
    NOT_FOUND = (404, "Not Found")
    INTERNAL_SERVER_ERROR = (500, "Internal Server Error")