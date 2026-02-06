from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from spm.database.core import Base
from spm.units.consts import UNIT
from spm.projects.models import Project
from spm.users.models import User

class Reffer(Base):
    __tablename__ = "reffers"

    id:Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    
    refferal_at:Mapped[datetime] = mapped_column(DateTime, nullable=False)
    project_id:Mapped[int] = mapped_column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"))
    from_user_id:Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    to_user_id:Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))

    project:Mapped[Project] = relationship("Project", foreign_keys=[project_id])
    user:Mapped[User] = relationship("User", foreign_keys=[to_user_id])

    @property
    def unit(self) -> UNIT:
        return self.user.unit

# pydantic models...
class UsersRefferals(BaseModel):
    projects: dict[
        int,
        list[UNIT]
    ]

class UsersOnProjectRefferals(BaseModel):
    project:int # project id
    units: list[UNIT]