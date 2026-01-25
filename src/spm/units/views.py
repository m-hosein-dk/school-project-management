from typing import Annotated
from fastapi import APIRouter, Path, Depends
from spm.units.consts import (
    UNIT
)
from .models import (
    UnitResponse
)
from spm.units import service as units_service

router = APIRouter()

UnitName = Annotated[UNIT, Path()]

@router.get(
    "", 
    response_model=list[UnitResponse],
)
def get_all_units():
    """Get all units."""
    return units_service.get_all_units()

@router.get(
    "/{unit_name}", 
    response_model=UnitResponse
)
def get_unit(unit_name: UnitName):
    """Get unit by name."""
    return units_service.get_unit(unit_name)