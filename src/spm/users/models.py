import bcrypt
from typing import Optional
from sqlalchemy import LargeBinary, BigInteger, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel
from spm.database.core import Base
from spm.units.consts import UNIT

def hash_password(password: str):
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)

# sqlalchemy models...
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)
    password: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)
    fullname: Mapped[str] = mapped_column(String(150), nullable=False)
    mobile: Mapped[str] = mapped_column(String(15), nullable=False)
    unit: Mapped[UNIT] = mapped_column(Enum(UNIT), nullable=False)

    def verify_password(self, password: str) -> bool:
        if not password or not self.password:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    def set_password(self, password: str) -> None:
        if not password:
            raise ValueError("Password cannot be empty")
        self.password = hash_password(password)

# pydantic models...
class CreateUser(BaseModel):
    username:str
    fullname:str
    mobile:str
    unit: UNIT
    password:str

class UserOut(BaseModel):
    username:str
    fullname:str
    mobile:str