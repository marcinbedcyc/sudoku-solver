from sqlalchemy import Boolean, Column, Integer, String

from fastapi_server.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    # Email is used for authentication that's why it is unique.
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
