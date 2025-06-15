from db import DBEngine, DataBase
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from typing import List, Annotated


async def lifspan(app_: FastAPI):
    e = DBEngine.create_engine('data')
    app_.state.db = DataBase()
    
    yield
    
    # app_.state.db.close()


app = FastAPI(
    debug=True,
    title='Приложение для контроля задач',
    lifespan=lifspan
)

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers import router_user, router_task

app.include_router(router_task, prefix="/api")
app.include_router(router_user, prefix="/api")