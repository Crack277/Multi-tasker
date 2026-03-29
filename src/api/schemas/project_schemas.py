from pydantic import BaseModel, Field


class CreateUserProject(BaseModel):
    name: str = Field(max_length=100)
    icon: str | None = Field(max_length=100)


class UpdateUserProject(CreateUserProject):
    id: int
    pass


class UserProject(CreateUserProject):
    owner_id: int
