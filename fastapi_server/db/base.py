# Import all the models, so that Base has them before being
# imported by Alembic
from fastapi_server.db.base_class import Base  # noqa
from fastapi_server.models.user import User  # noqa
