from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    password: str
    role: str = "user"