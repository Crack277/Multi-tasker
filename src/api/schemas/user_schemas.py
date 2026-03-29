from pydantic import BaseModel, EmailStr, Field


class UserUpdate(BaseModel):
    email: EmailStr


class UserLoging(UserUpdate):
    password: str = Field(min_length=8, max_length=16)


class UserCreate(UserLoging):
    repeat_password: str = Field(min_length=8, max_length=16)


class PrintUserInfo(BaseModel):
    user_id: int
    email: EmailStr


class PrintAccessToken(BaseModel):
    access_token: str
    type: str = "Bearer"


class AuthUpdatePassword(BaseModel):
    old_password: str = Field(min_length=8, max_length=16)
    new_password: str = Field(min_length=8, max_length=16)
    repeat_new_password: str = Field(min_length=8, max_length=16)


class UnAuthUpdatePassword(BaseModel):
    confirm_code: str = Field(min_length=6, max_length=6)
    new_password: str = Field(min_length=8, max_length=16)
    repeat_new_password: str = Field(min_length=8, max_length=16)
