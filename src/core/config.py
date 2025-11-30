from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "Guardião Digital"

    GOOGLE_SAFE_BROWSING_KEY: str | None = Field(default=None)
    VIRUSTOTAL_KEY: str | None = Field(default=None)

    ENV: str = Field(default="development")
    DATABASE_URL: str | None = Field(default=None)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        validate_default=True
    )

settings = Settings()
