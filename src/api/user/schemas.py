from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)


class UserCreate(UserBase):
    repeat_password: str = Field(min_length=8, max_length=16)


class UserUpdate(UserBase):
    pass


class UserLoging(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)
