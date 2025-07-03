from typing import Optional

from pydantic import BaseModel, UUID4

class User(BaseModel):
    id: Optional[UUID4] = None
    name: str
    email: str
    gender: bool
    age: int

class CreateUser(BaseModel):
    name: str
    email: str
    gender: bool
    age: int

class UpdateUser(BaseModel):
    name: Optional[str] = None
    gender: Optional[bool] = None
    age: Optional[int] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
