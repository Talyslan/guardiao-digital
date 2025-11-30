import os
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Guardião Digital"
    GOOGLE_SAFE_BROWSING_KEY: str | None = os.getenv('GOOGLE_SAFE_BROWSING_KEY')
    VIRUSTOTAL_KEY: str | None = os.getenv('VIRUSTOTAL_KEY')
    ENV: str = "development"
    DATABASE_URL: str | None = None

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
