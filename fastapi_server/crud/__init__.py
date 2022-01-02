from fastapi_server.crud.user import user  # noqa

# For a new basic set of CRUD operations you could just do

# from fastapi_server.crud.base import CRUDBase
# from fastapi_server.models.item import Item
# from fastapi_server.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
