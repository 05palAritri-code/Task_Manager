from fastapi import APIRouter, Depends , status ,Request
from sqlalchemy.orm import Session
from user_dtos import UserResponseSchema, UserSchema , UserLoginSchema
import user_controller
from user_dtos import UserSchema
from utils.db import get_db

user_routes = APIRouter(prefix="/api/v1/users",
    tags=["users"])

@user_routes.post("/register" ,response_model= UserResponseSchema ,status_code=status.HTTP_201_CREATED)
def register_user(body: UserSchema, db: Session = Depends(get_db)):
    return user_controller.register(body, db)
 
@user_routes.post("/login", status_code=status.HTTP_200_OK)
def login_user(body: UserLoginSchema, db: Session = Depends(get_db)):
    return user_controller.login_user(body, db)

@user_routes.get("/is_authenticated",status_code=status.HTTP_200_OK)
def is_auth(request : Request, db: Session = Depends(get_db)):
    return user_controller.is_authenticated(request,db)