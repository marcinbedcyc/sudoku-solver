# import secrets
import os

from pydantic import BaseSettings

OEG = os.environ.get
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)


class Settings(BaseSettings):
    # 1 day * 24 hours * 60 minutes = 1 day
    ACCESS_TOKEN_EXPIRE_MINUTES = 1 * 24 * 60
    API_V1_STR = '/api/v1'
    PROJECT_NAME = 'Sudoku Solver'
    # Change to `secrets.token_urlsafe(32)` later or load from envs
    SECRET_KEY = OEG(
        'SECRET_KEY',
        'Z7dB4UikAcpG2VU7HHHOH-yifGtMPp3RJe08jon2MGw'
    )
    SQL_ALCHEMY_DATABASE_URI = OEG(
        'SQL_ALCHEMY_DATABASE_URI',
        f'sqlite:///{os.path.join(BASE_DIR, "sqlite3.db")}'
    )

    class Config:
        case_sensitive = True


settings = Settings()
