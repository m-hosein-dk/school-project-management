from pydantic import BaseModel
from .consts import UNIT

# pydantic models...
class UnitIn(BaseModel):
    name: UNIT
    language: str | None = None

class UnitResponse(BaseModel):
    name: UNIT
    language_mapping: dict[str, str]