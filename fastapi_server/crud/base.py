from typing import Any, Dict, Generic, List, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from fastapi_server.db.base_class import Base


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> ModelType:
        return db.query(self.model).get(id)

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, input: CreateSchemaType) -> ModelType:
        obj_input_data = jsonable_encoder(input)
        db_object = self.model(**obj_input_data)
        db.add(db_object)
        db.commit()
        db.refresh(db_object)
        return db_object

    def update(
        self,
        db: Session, *,
        db_object: ModelType,
        input: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        data = jsonable_encoder(db_object)
        update_data = input if isinstance(input, dict) else input.dict(
            exclude_unset=True
        )

        for field in data:
            if field in update_data:
                setattr(db_object, field, update_data[field])

        db.add(db_object)
        db.commit()
        db.refresh(db_object)
        return db_object

    def remove(self, db: Session, *, id: Any) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
