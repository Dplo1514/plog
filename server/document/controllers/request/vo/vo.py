from pydantic import BaseModel, Field


class UploadFileVo(BaseModel):
    file_name: str
    file_size: int = Field(..., ge=1)
    chunk_size: int = Field(1024 * 1024, ge=1)

    class Config:
        frozen = True