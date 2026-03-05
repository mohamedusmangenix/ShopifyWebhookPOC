from pydantic import BaseModel
from typing import Any

class ShopifyToken(BaseModel):
    token:str
    scopes:str
    expire_in:int