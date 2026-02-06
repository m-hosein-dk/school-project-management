from pydantic import BaseModel
from sqlalchemy import ForeignKey, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from spm.database.core import Base

class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))

    path: Mapped[str] = mapped_column(String(100))
    file_name: Mapped[str] = mapped_column(String(100))

# pydantic models ...
class FileOut(BaseModel):
    file_name: str
    file_size: int
    project_id: int
    mime_type: str
    path: str