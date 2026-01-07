from typing import Literal
from pydantic import BaseModel

# pydantic models...
class SearchPaginationInputs(BaseModel):
    q: str
    sortby: str = "id"
    order: Literal["asc", "desc"] = "asc"
    page:int = 1
    page_size:int = 10

class SearchPaginationOutput(BaseModel):
    total_count: int
    total_pages: int
    current_page: int
    page_size: int