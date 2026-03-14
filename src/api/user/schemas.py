from pydantic import BaseModel, EmailStr, Field
from pydantic_settings import SettingsConfigDict


class UserBase(BaseModel):
    email: EmailStr
    hashed_password: str = Field(min_length=8, max_length=16)

class UserCreate(UserBase):
    reset_password: str = Field(min_length=8, max_length=16)



class UserUpdate(UserBase):
    pass


class User(UserBase):

    id: int = SettingsConfigDict(from_attributes=True)

    # project: List[]
