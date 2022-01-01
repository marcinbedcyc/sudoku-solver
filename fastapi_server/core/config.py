import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY = secrets.token_urlsafe(32)
    SQL_ALCHEMY_DATABASE_URI = "sqlite:///./sqlite3.db"

    # 1 day * 24 hours * 60 minutes = 1 day
    ACCESS_TOKEN_EXPIRE_MINUTES = 1 * 24 * 60

    class Config:
        case_sensitive = True


settings = Settings()
