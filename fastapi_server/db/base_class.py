from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any

    # Auto-generated table name
    @declared_attr
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'
