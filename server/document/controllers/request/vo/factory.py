from server.document.controllers.request.vo.vo import UploadFileVo
from server.document.controllers.request.dto.dto import UploadFileDTO


def upload_file_vo_factory(
    request_dto: UploadFileDTO
) -> UploadFileVo:
    return UploadFileVo(
        file_name=request_dto.file_name,
        chunk_size=int(request_dto.chunk_size),
        file_size=int(request_dto.file_size)
    )
