from .engine import DBEngine
from abc import ABC, abstractmethod
import hashlib
import time 
from typing import List
from datetime import timedelta, datetime


class BaseDBModel(ABC):
    _e: DBEngine
    fields = tuple()
    
    def __init__(self):
        self._e = DBEngine.get_engine()
    
    def get_fields(self) -> dict:
        data = {}
        for f in self.fields:
            data[f] = getattr(self, f)
        return data
    
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f"{k}={v}" for k, v in self.get_fields().items()])})"
    
    @abstractmethod
    def save(self):
        pass

class User(BaseDBModel):
    fields = ('id', 'login', 'password_hash')
    
    def __init__(
        self, 
        id: int,
        login: str,
        password_hash: str,
    ):
        super().__init__()
        
        self.id: int = id
        self.login: str = login
        self.password_hash: str = password_hash
        
        self.reg_cookie: str | None = None
    
    
    def save(self):
        self._e.update_user(self.id, **self.get_fields())
        
    def check_password(self, password:str) -> bool:
        hsh = hashlib.sha256(password.encode()).hexdigest()
        return self.password_hash == hsh
    
    def set_password(self, new_password:str):
        self.password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        
    def set_cookie(self) -> str:
        cookie = self._e.create_cookie(self.id, expire=time.time() + timedelta(weeks=3).total_seconds())
        self.reg_cookie = cookie
        return cookie
    
    def unset_cookie(self):
        self._e.remove_cookie(self.id, self.reg_cookie)
        self.reg_cookie = None
        
    def get_tasks(self, time_from: int=None, time_to: int=None, **kwargs) -> List['Task']:
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        
        kwargs['user_id'] = self.id
        tasks = [Task(**data) for data in self._e.find_tasks(**kwargs)]
        time_from = time_from or 0
        time_to = time_to or 2500000000
        return sorted([t for t in tasks if time_from <= t.deadline <= time_to], key=lambda x: x.deadline)
        
    
    


class Task(BaseDBModel):
    fields = ('id', 'user_id', 'title', 'text', 'priority', 'deadline', 'created')
    
    def __init__(
        self, 
        id: int,
        user_id: int,
        title: str,
        text: str,
        priority: int = 0,
        deadline: int | None = None,
        created: int | None = None
    ):
        super().__init__()
        
        self.id: int = id
        self.user_id: int = user_id
        self.title: str = title
        self.text: str = text
        self.priority: int = priority
        self.deadline: int | None = deadline
        self.created: int = int(created) if created is not None else int(time.time())
        
    def save(self):
        self._e.update_task(self.id, **self.get_fields())

    def delete(self):
        self._e.delete_task(self.id)


