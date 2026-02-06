import os

def env(name:str, default:str | None = None):
    if default is not None:
        return os.environ.get(name, default)
    else:
        env = os.environ.get(name)

        if not env:
            raise ValueError(f'"{name}" needs to be set as an environment variable')
        
        return env


DATABASE_URL = env("SPM_DATABASE_URL")

JWT_SECRET = env("JWT_SECRET")
JWT_ALGORITHM = env("JWT_ALGORITHM", "HS256")

DEFAULT_USERNAME = env("DEFAULT_USERNAME")
DEFAULT_PASSWORD = env("DEFAULT_PASSWORD")
DEFAULT_MOBILE = env("DEFAULT_MOBILE")
DEFAULT_FULLNAME = env("DEFAULT_FULLNAME")

FILES_PATH = env("FILES_PATH")