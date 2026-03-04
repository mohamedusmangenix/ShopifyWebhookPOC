from pydantic import BaseModel
from typing import Any

class ResponseModel(BaseModel):
    data: dict | list | Any | None = None
    status: str
    is_success: bool
    message: str | None = None