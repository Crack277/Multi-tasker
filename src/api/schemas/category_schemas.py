from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(max_length=100)
    marker: str = Field(min_length=7, max_length=7)

class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass