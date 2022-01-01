from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi_server.core.config import settings


engine = create_engine(
    settings.SQL_ALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
