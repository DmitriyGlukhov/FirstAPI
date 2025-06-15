from pydantic import BaseModel, Field
from typing import List

class AuthData(BaseModel):
    login: str = Field(..., max_length=50, description='Ваш логин')
    password: str = Field(..., description='Ваш пароль')


class CreateTaskData(BaseModel):
    title: str = Field(..., description='Заголовок')
    text: str = Field(..., description='Текст задачи')
    priority: int = Field(0, ge=0, le=3, description="Приоритет")
    deadline: int = Field(..., description="Выполнить до")
    
class ResponseTaskData(CreateTaskData):
    id: int = Field(..., description='')
    user_id: int = Field(..., description='')
    created: int = Field(..., description='')

class ResponseTasks(BaseModel):
    tasks: List[ResponseTaskData] = Field(..., description='Список ID задач')

class ResponseUserData(BaseModel):
    id: int = Field(..., description='')
    login: str = Field(..., description="")