# берет schemas и вызывает функции из repository

from typing import List, Optional
from ..repository import user_re
from ..repository.user_re import UserAlreadyExistsError
from ..schemas.user_she import User, UserCreate, UserUpdate

class UserService:
    def add_user(self, user_data: UserCreate) -> User:
        try:
            user_id = user_re.add_user(
                name=user_data.name,
                email=user_data.email,
                age=user_data.age
            )
            user_dict = user_re.read_user(user_id=user_id)[0] # получить данные нового юзера
            return User(**user_dict)  # Создать Pydantic модель из словаря
        except UserAlreadyExistsError as e:
            print(f"Service layer caught an error: {e}")
            raise e

    def read_user(self, user_id: int = None, name: str = None) -> list[User]:
        user_dict = user_re.read_user(user_id=user_id, name=name)
        return [User(**user_dict) for user_dict in user_dict]

    def update_user(self, user_id: int, user: UserUpdate) -> Optional[User]:
        updates = user.dict(exclude_unset=True)
        if not updates:
            return None
        updated_rows = user_re.update_user(user_id, updates)
        if updated_rows == 0:
            return None

        user_dict = user_re.read_user(user_id=user_id)[0]
        return User(**user_dict)

    def delete_user(self, user_id: int) -> bool:
        deleted_count = user_re.delete_user(user_id)
        return deleted_count > 0

user_service = UserService()