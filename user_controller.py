from sqlalchemy.orm import Session
from user_dtos import UserSchema,UserLoginSchema
from tables import  UserModel
from fastapi import HTTPException,status,Request,Depends
from pwdlib import PasswordHash
import jwt
from utils import settings
from utils.settings import settings
from datetime import datetime , timedelta
from utils.db import get_db

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def register(body: UserSchema, db: Session):

    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )
    
    password_hash = get_password_hash(body.password)
    new_user = UserModel(username=body.username, password=password_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
    "success": True,
    "message": "User registered successfully",
    "data": {
        "id": new_user.id,
        "username": new_user.username
    }
}

def login_user(body : UserLoginSchema , db: Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username is incorrect"
        )

    if not verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)
    token = jwt.encode({"id":user.id , "exp":exp_time},settings.SECRET_KEY , settings.ALGORITHM)

    return {
    "success": True,
    "message": "Login successful",
    "data": {
        "token": token,
        "username": user.username
    }
}

def is_authenticated(request: Request, db: Session):
    token = request.headers.get("authorization")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is Unauthenticated"
        )

    token = token.split(" ")[1]

    try:
        data = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user_id = data.get("id")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user

