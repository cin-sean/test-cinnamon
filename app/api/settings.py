from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SUPPORT_TYPES: Optional[List[str]] = Field(
        default=None,
        description="List support file extensions",
        examples=[[".pdf", ".png", ".jpg"]],
    )


settings = Settings()
