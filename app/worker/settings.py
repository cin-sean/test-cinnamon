from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SOFT_TIME_LIMIT: int = 5
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 3


settings = Settings()
