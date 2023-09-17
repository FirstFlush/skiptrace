from pydantic import BaseModel, Field
from typing import Optional


class SpiderSchema(BaseModel):
    spider_name: str = Field(..., max_length=255)
    is_active: Optional[bool]
    description: Optional[str] = Field(..., max_length=2048)

    class Config:
        exclude_unset = True