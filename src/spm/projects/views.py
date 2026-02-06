from fastapi import APIRouter, Depends
from spm.core import DbSession
from spm.permissions import (
    PermissionsDependency
)
from spm.users.permissions import (
    SystemAdministrator
)
from spm.users.service import CurrentUser
from .models import (
    CreateProject
)
from . import service as project_service

router = APIRouter()

@router.get("/properties")
def get_project_properties_by_unit(
    user: CurrentUser,
    project: int,
    session: DbSession
):
    return project_service.get_project_properties_by_unit(
        project,
        user.unit,
        session
    )

@router.post("",
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
def create_project(
    user: CurrentUser,
    model: CreateProject,
    session: DbSession
):
    return project_service.create_project(
        user,
        model,
        session
    )