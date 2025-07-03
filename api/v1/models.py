from typing import Optional

from pydantic import BaseModel, UUID4, EmailStr, SecretStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: SecretStr
    name: str
    gender: bool
    age: int


class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[SecretStr] = None
    gender: Optional[bool]
    age: Optional[int]
    is_active: Optional[bool]
    is_superuser: Optional[bool]


class UserInDB(UserBase):
    id: UUID4
    name: str
    gender: bool
    age: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
