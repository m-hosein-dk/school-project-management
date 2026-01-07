import os

DATABASE_URL = os.environ.get("SPM_DATABASE_URL")

JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")

DEFAULT_USERNAME = os.environ.get("DEFAULT_USERNAME")
DEFAULT_PASSWORD = os.environ.get("DEFAULT_PASSWORD")