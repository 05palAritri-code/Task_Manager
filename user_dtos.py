from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    password: str
    
class UserResponseSchema(BaseModel):
    id: int
    username: str
    
class UserLoginSchema(BaseModel):
    username: str
    password: str