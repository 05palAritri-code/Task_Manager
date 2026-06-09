from sqlalchemy.orm import Session
from user_dtos import UserSchema

def register(body: UserSchema, db: Session):
    return {"message": "User registered successfully"}