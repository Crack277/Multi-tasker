from pydantic import BaseModel, EmailStr


class ProfileBase(BaseModel):
    name: str
    email: EmailStr
    photo: str


class ProfileCreate(ProfileBase):
    pass

