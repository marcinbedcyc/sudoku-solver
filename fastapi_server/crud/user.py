from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from fastapi_server.core.security import get_password_hash, verify_password
from fastapi_server.crud.base import BaseCRUD
from fastapi_server.models.user import User
from fastapi_server.schemas.user import UserCreate, UserUpdate


class UserCRUD(BaseCRUD[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, user_in: UserCreate) -> User:
        db_user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            is_superuser=user_in.is_superuser
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(
        self,
        db: Session,
        *,
        user_db: User,
        user_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        update_data = user_in if isinstance(user_in, dict) else user_in.dict(
            exclude_unset=True
        )
        if update_data.get('password'):
            hashed_password = get_password_hash(update_data['password'])
            del update_data['password']
            update_data['hashed_password'] = hashed_password
        return super().update(db, db_object=user_db, input=update_data)

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[User]:
        user = self.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = UserCRUD(User)
