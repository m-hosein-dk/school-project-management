from sqlalchemy import create_engine
from spm import config

engine = create_engine(
    config.DATABASE_URL,
)