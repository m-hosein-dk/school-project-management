from datetime import datetime
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from spm.units.consts import UNIT
from spm.users import service as users_service
from .models import (
    Reffer,
    UsersRefferals,
    UsersOnProjectRefferals
)

def users_refferals(user_id: int, session: Session) -> UsersRefferals:
    refferals = session.query(Reffer).filter(
        Reffer.to_user_id == user_id,
    ).all()

    results = UsersRefferals(projects={})

    for refferal in refferals:
        if refferal.project_id not in results.projects:
            results.projects[refferal.project_id] = []    
        results.projects[refferal.project_id].append(refferal.unit)

    return results

def users_refferaled_projects_units(
    user_id: int,
    project: int,
    session: Session
) -> UsersOnProjectRefferals:
    refferals = session.query(Reffer).filter(
        Reffer.to_user_id == user_id,
        Reffer.project_id == project
    ).all()

    return UsersOnProjectRefferals(
        project=project,
        units = [refferal.unit for refferal in refferals]
    )

def user_has_refferal_on_project(user_id: int, project_id: int, session: Session) -> bool:
    return session.query(Reffer).filter(
        Reffer.to_user_id == user_id,
        Reffer.project_id == project_id
    ).first() is not None

def unit_has_refferal_on_project(unit: UNIT, project_id: int, session: Session) -> bool:
    refferal = session.query(Reffer).join(Reffer.user).filter(
        Reffer.project_id == project_id
    ).first()

    if refferal and refferal.unit == unit:
        return True
    return False

def remove_refferal_from(
    user_id: int,
    project_id: int,
    session: Session
):
    old_refferal = session.query(Reffer).filter(
        Reffer.to_user_id == user_id,
        Reffer.project_id == project_id
    ).one()

    if old_refferal:
        session.delete(old_refferal)

def refferal_user_to(
    from_user_id:int, 
    to_user_id:int, 
    project_id:int,
    session:Session,
    expection_unit: UNIT | None = None
):
    target_user = users_service.get_user(to_user_id, session)

    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="target user not found."
        )

    if target_user.unit != expection_unit:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"target user {to_user_id} expected to be in unit {expection_unit}"
        )

    if unit_has_refferal_on_project(target_user.unit, project_id, session):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, 
            detail="project already has refferes on this unit."
        )

    if user_has_refferal_on_project(to_user_id, project_id, session):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, 
            detail="target user already has refferal on this project."
        )

    requesting_user = users_service.get_user(from_user_id, session)

    if not requesting_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    new_refferal = Reffer(
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        project_id=project_id,
        refferal_at=datetime.now()
    )
    session.add(new_refferal)