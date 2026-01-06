from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from spm import config

engine = create_engine(
    config.DATABASE_URL,
)

class Base(DeclarativeBase):
    pass

def create_all():
    Base.metadata.create_all(engine)