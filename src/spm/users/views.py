from fastapi import APIRouter, Depends, HTTPException
from spm.core import DbSession
from spm.permissions import PermissionsDependency
from spm.database.core import SearchPaginationParameters
from spm.database import service as database_service
from .permissions import (
    SystemAdministrator,
    GeneralManager
)
from .models import (
    CreateUser,
    User
)
from . import service as users_service

router = APIRouter()

@router.post(
    "",
    dependencies=[
        Depends(
            PermissionsDependency(
                [
                    SystemAdministrator
                ]
            )
        )
    ]
)
def create_user(input_user:CreateUser, session:DbSession):
    "only callable by system administrators"
    existing_user = users_service.get_user_by_username(input_user.username, session)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="A user with this username already exists."
        )

    users_service.create_user(
        input_user,
        session
    )

@router.get(
    "",
    dependencies=[
        Depends(
            PermissionsDependency([
                GeneralManager
            ])
        )
    ],
    response_model=dict[str, str | int | list[dict[str, str | int]]]
)
def view_users_paginiaion(input: SearchPaginationParameters, session:DbSession):
    "only callable by system administrators and general managers"
    paginiation_info, items = database_service.search_pagination(
        User,
        input,
        session
    )

    return {
        "users": [
            {
                "id": it.id,
                "username": it.username,
                "fullname": it.fullname,
                "mobile": it.mobile,
            }
            for it in items
        ],
        "page_size": paginiation_info.page_size,
        "current_page": paginiation_info.current_page,
        "total": paginiation_info.total_count,
        "total_pages": paginiation_info.total_pages,
    }