# берет schemas и вызывает функции из repository

from typing import List, Optional
from ..repository import user_re
from ..schemas.user_she import User, UserCreate, UserUpdate

class UserService:
    def create_user(self, user: UserCreate) -> User:
        user_id = user_re.add_user(
            name=user.name,
            email=user.email,
            age=user.age
        )
        user_dict = user_re.find_users_by(user_id=user_id)[0] # получить данные нового юзера
        return User(**user_dict)  # Создать Pydantic модель из словаря

    def read_user(self, user_id: int = None, name: str = None) -> list[User]:
        user_dict = user_re.find_users_by(user_id=user_id, name=name)
        return [User(**user_dict) for user_dict in user_dict]

    def update_user(self, user_id: int, user: UserUpdate) -> Optional[User]:
        updates = user.dict(exclude_unset=True)
        if not updates:
            return None
        updated_rows = user_re.update_user(user_id, updates)
        if updated_rows == 0:
            return None

        user_dict = user_re.find_users_by(user_id=user_id)[0]
        return User(**user_dict)

    def delete_user(self, user_id: int) -> bool:
        deleted_count = user_re.delete_user(user_id)
        return deleted_count > 0

user_service = UserService()