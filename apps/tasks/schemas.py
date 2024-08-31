from enum import Enum
from typing import Optional
from pydantic import BaseModel, field_validator, EmailStr, Field, HttpUrl

class StatusType(str, Enum):
    DONE = 'done'
    PENDING = 'pending'


class Category(BaseModel):
    id: int
    name: str

class CreateCategorySchema(BaseModel):
    name: str

class User(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    website: HttpUrl

class CreateUserSchema(BaseModel):
    name: str
    username: str = Field(min_length=6) # Se puede agregar validaciones con el metodo Field
    email: EmailStr
    website: str = HttpUrl


class TaskSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] | None = Field(default="Sin Descripción", max_length=100)
    status: StatusType
    category: Category
    user: User
    # tags: List[str] = [] # Es una lista de elementos
    # tags: set[str] | None = set() # Es una lista de elementos únicos, si se repite un elemento, solo se guarda una vez
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": [
                {
                    "id": 1,
                    "name": "Task 1",
                    "description": "Description",
                    "status": StatusType.PENDING,
                    "category": {
                        "id": 1,
                        "name": "Category 1"
                    },
                    "user": {
                        "id": 1,
                        "name": "User 1",
                        "username": "user1",
                        "email": "test@tes.com",
                        "website": "https://www.user1.com"
                    },
                    "tags": ["tag1", "tag2"]
                },
            ]
        }
    
    @field_validator('name')
    def name_alphanumerics_whitespace(cls, v: str):
        if v:
            v = v.replace(' ', '')
            return v
        raise ValueError('Name must be alphanumeric')

class TaskCreateSchema(BaseModel):
    name: str
    description: Optional[str] | None = Field("Sin Descripción", max_length=100)
    status: StatusType
    category: int
    user: int

