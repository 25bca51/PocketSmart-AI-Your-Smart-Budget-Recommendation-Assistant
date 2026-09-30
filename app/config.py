from functools import lru_cache
from importlib import import_module

try:
    _pydantic_settings = import_module("pydantic_settings")
    BaseSettings = _pydantic_settings.BaseSettings
    SettingsConfigDict = _pydantic_settings.SettingsConfigDict
    _USE_PYDANTIC_SETTINGS = True
except ImportError:
    from pydantic import BaseSettings  # pyright: ignore[reportMissingImports]

    SettingsConfigDict = dict
    _USE_PYDANTIC_SETTINGS = False


class Settings(BaseSettings):
    APP_NAME: str = "PocketSmart AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    SECRET_KEY: str = "change-this-secret-key-in-production"
    DATABASE_URL: str = "sqlite:///./pocketsmart.db"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    MAX_IMAGE_SIZE_MB: int = 5
    ALLOWED_ORIGINS: str = "*"

    if _USE_PYDANTIC_SETTINGS:
        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            case_sensitive=True,
            extra="ignore",
        )
    else:
        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"
            case_sensitive = True
            extra = "ignore"

    @property
    def allowed_origins_list(self):
        if self.ALLOWED_ORIGINS.strip() == "*":
            return ["*"]

        return [
            origin.strip()
            for origin in self.ALLOWED_ORIGINS.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()