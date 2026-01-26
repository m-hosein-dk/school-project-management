from fastapi import APIRouter
from .models import (
    UsernamePasswordLogin,
    ChangePassword,
)
from spm.core import DbSession
from spm.users.service import CurrentUser
from spm.users import service as users_service
from spm.auth import service as auth_service

router = APIRouter()

@router.post(
    "/password",
)
def login_by_username_password(
    credentials: UsernamePasswordLogin,
    session: DbSession
):
    return auth_service.username_password_login(credentials, session)

@router.post(
    "/password/change"
)
def change_password_by_old_password(
    model: ChangePassword,
    user: CurrentUser,
):
    "changes the password only if current password is givin currectly"
    return auth_service.change_password(
        model,
        user,
    )