from pydantic import BaseModel, EmailStr, Field


class ProfileBase(BaseModel):
    name: str = Field(min_length=8, max_length=16)
    email: EmailStr
    photo: str


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass
