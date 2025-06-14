from typing import Optional, List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SUPPORT_TYPES: Optional[List[str]] = Field(
        None,
        description="List support file extensions",
        example=[".pdf", ".png", ".jpg"],
    )

settings = Settings()