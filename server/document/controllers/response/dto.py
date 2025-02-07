from pydantic import BaseModel, Field
from flask import request, jsonify


class UploadFileDTO(BaseModel):
    file_name: str = Field(..., alias="file_name")
    file_size: int = Field(..., alias="file_size", ge=1)
    chunk_size: int = Field(1024 * 1024, alias="chunk_size", ge=1)
