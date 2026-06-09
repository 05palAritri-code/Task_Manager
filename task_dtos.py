from pydantic import BaseModel


class TaskSchema(BaseModel):
    title: str
    description: str
    status: bool = False

class TaskUpdateSchema(BaseModel):
    id : int
    title: str
    description: str
    status: bool