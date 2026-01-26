import logging
import jwt
from spm.config import (
    JWT_SECRET,
    JWT_ALGORITHM
)
from spm.users.models import User

log = logging.getLogger(__name__)

def gen_jwt_for_user(user:User):
    payload = {
        "user_id": user.id,
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def get_id_from_jwt(token:str):
    payload = jwt.decode(token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])

    try:
        return payload["user_id"]
    except KeyError as e:
        log.info("couldn't get users id from jwt payload:\n"f"{payload}")
        raise e from None

def authorization_params(auth_headers):
    if auth_headers:
        type, _, token =auth_headers.partition(" ")
        return type, token

    return "", ""