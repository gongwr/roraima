from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import Row

from roraima.db.models import RoraimaBase
from roraima.db.sqlalchemy.api import get_session

ModelType = TypeVar("ModelType", bound=RoraimaBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, id: Any) -> Optional[ModelType]:
        db = get_session()
        with db.begin():
            return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
            self, *, skip: int = 0, limit: int = 100
    ) -> list[Row[tuple[Any]]]:
        db = get_session()
        with db.begin():
            return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        db = get_session()
        with db.begin():
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)  # type: ignore
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

    def update(
            self,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        db = get_session()
        obj_data = jsonable_encoder(db_obj)
        with db.begin():
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

    def remove(self, *, id: int) -> ModelType:
        db = get_session()
        with db.begin():
            obj = db.query(self.model).get(id)
            db.delete(obj)
            db.commit()
            return obj
