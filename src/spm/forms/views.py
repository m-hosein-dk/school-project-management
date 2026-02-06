from typing import Annotated, Any
from fastapi import APIRouter, Form, Request
from spm.core import DbSession
from spm.users.service import CurrentUser
from spm.units.consts import UNIT
from .models import (
    FormIn,
    AllForms
)
from . import service as forms_service

router = APIRouter()

@router.get("")
def get_all_forms(
    user: CurrentUser,
    session: DbSession
) -> AllForms:
    "returns all forms from all projects and their units"
    return forms_service.forms_hierarchy(user.id, session)

@router.get("/unit/{unit}")
def get_unit_form(unit: UNIT):
    "returns units form"
    return forms_service.get_unit_form(unit)

@router.get("/projects")
def get_projects_with_forms(
    user: CurrentUser,
    session: DbSession
):
    "returns projects and units that has form"
    return forms_service.get_projects_units_with_form(
        user.id,
        session
    )

@router.get("/project")
def get_projects_units_forms(
    user: CurrentUser,
    project: int,
    session: DbSession
):
    "returns units from reffered project"
    return forms_service.get_project_units_with_form(
        user.id,
        project,
        session
    )

@router.post("")
async def submit_form(
    user: CurrentUser,
    project_id: int,
    request: Request,
    session: DbSession
):
    "submits form to project"
    request_form = dict(await request.form())
    return forms_service.submit_form(
        user,
        form_in=FormIn(
            project_id=project_id,
            input = request_form
        ),
        session=session
    )