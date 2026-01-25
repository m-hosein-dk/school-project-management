from typing import Annotated
import logging
from fastapi import Request, Depends
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from spm.config import (
    DEFAULT_USERNAME,
    DEFAULT_PASSWORD,
    DEFAULT_FULLNAME,
    DEFAULT_MOBILE
)
from spm.units.consts import UNIT
from spm.users.models import (
    User,
    CreateUser,
)

log = logging.getLogger(__name__)

def get_user(id:int, session:Session):
    return session.query(User).filter(User.id == id).one_or_none()

def get_user_by_username(username:str, session:Session):
    return session.query(User).filter(User.username == username).one_or_none()

def create_user(input_user: CreateUser, session:Session):
    # if were here, were going to assume that we have the permissions
    user = User(
        username = input_user.username,
        mobile = input_user.mobile,
        fullname = input_user.fullname,
        unit = input_user.unit,
    )
    user.set_password(input_user.password)
    
    log.info("adding user with username {0} to database".format(input_user.username))
    session.add(user)

    return user

def create_default_user(session:Session):
    "creates the default admin user"
    log.info("creating default admin user")
    existing_user = get_user_by_username(DEFAULT_USERNAME, session)
    if existing_user:
        log.info("create_default_user: an existing user with username {0} already exists, aborting.".format(DEFAULT_USERNAME))
        return existing_user

    user = User(
        username=DEFAULT_USERNAME,
        mobile=DEFAULT_MOBILE,
        fullname=DEFAULT_FULLNAME,
        unit=UNIT.SYSTEM_ADMINISTRATOR,
    )

    log.info("setting password for default user")
    user.set_password(DEFAULT_PASSWORD)

    log.info("adding default user to database")
    session.add(user)

    return user

def change_password(user:User, old_password:str, new_password:str, session:Session):
    if not user.verify_password(old_password):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "wrong password"
        )
    
    user.set_password(new_password)

def get_current_user(request:Request) -> User | None:
    # request.state.user is going to be set by auth module
    user:User | None = getattr(request.state, "user", None)
    if user:
        if not user.password:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "current user doesnt have a password. current user needs to set a password"
            )
    else:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Unathorized"
        )
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]