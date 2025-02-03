from server.common.status import BaseStatus


class DocumentSuccessStatus(BaseStatus):
    code: int
    message: str

    FILE_UPLOAD_SUCCESS = (3001, "Operation Success")

class DocumentErrorStatus(BaseStatus):
    code: int
    message: str

    FILE_UPLOAD_FAILURE = (3002, "Internal Server Error")
