from .engine import DBEngine
from .models import User, Task
from .errors import UserAlreadyExists
import hashlib
from fastapi import HTTPException

class DataBase:
    _e: DBEngine
    
    def __init__(self):
        self._e = DBEngine.get_engine()
        
    def create_user(self, login: str, password: str) -> User:
        old = self._e.find_one_user(login=login)
        if old:
            return None
        user = User(-1, login, '')
        user.set_password(password)
        new_id = self._e.create_user(**user.get_fields())
        user.id = new_id
        return user
    
    def get_user(self, id: int) -> User | None:
        data = self._e.get_user_data(id)
        if data:
            return User(**data)
        
    def auth_user_by_cookie(self, cookie: str) -> User | None:
        user_id = self._e.get_user_id_by_cookie(cookie)
        if user_id is None:
            print(f"user_id none")
            return
        user = self.get_user(user_id)
        if user is None:
            return None
        user.reg_cookie = cookie
        return user
        
    
    def auth_user_by_login_pass(self, login: str, password: str):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user_data = self._e.find_one_user(login=login, password_hash=password_hash)
        if user_data is None:
            return None
        return User(**user_data)
    

    def create_task(
        self,
        user_id: int,
        title: str,
        text: str,
        priority=0,
        deadline=None,
        created=None
    ) -> Task:
        task = Task(-1, user_id, title, text, priority, deadline, created)
        new_id = self._e.create_task(**task.get_fields())
        task.id = new_id
        return task
    
    def get_task(self, id: int) -> Task | None:
        data = self._e.get_task_data(id)
        if data:
            return Task(**data)
        