from fastapi import APIRouter
from sqlalchemy.orm import Session
from user_dtos import UserSchema
from user_controller import register

user_routes = APIRouter(prefix="/api/v1/users",
    tags=["users"])

@user_routes.post("/register")
def register_user(body: UserSchema, db: Session):
    return register(body, db)