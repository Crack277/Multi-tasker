from pydantic import BaseModel


class Pagination(BaseModel):
    page: int
    page_size: int