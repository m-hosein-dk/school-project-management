from datetime import datetime
from sqlalchemy import Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import BaseModel
from spm.database.core import Base

# pydantic models...
class HelloResponse(BaseModel):
	hello:str