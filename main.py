from fastapi import FastAPI
from utils.db import Base, engine
from task_route import task_routes
from user_routes import user_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)

app = FastAPI(title="Task Manager", )

app.include_router(task_routes)

app.include_router(user_routes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)