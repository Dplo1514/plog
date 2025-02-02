from typing import Optional, Union

from pydantic import BaseModel, Field


class Response(BaseModel):
    code: int
    message: str
    data: Optional[Union[dict, str]] = Field(
        None,
        description="detail information if it exsits"
    )
