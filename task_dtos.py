from pydantic import BaseModel, Field, field_validator

class TaskSchema(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=5, max_length=300)
    status: bool = False

    @field_validator("title", "description")
    @classmethod
    def clean_strings(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Field cannot be empty")
        return v

class TaskUpdateSchema(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=5, max_length=300)
    status: bool

    @field_validator("title", "description")
    @classmethod
    def clean_strings(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Field cannot be empty")
        return v