from typing import Annotated
from fastapi import APIRouter, Path, Depends
from spm.units.consts import (
    UNIT
)
from .models import (
    AllUnitsResponse
)
from spm.units import service as units_service

router = APIRouter()

UnitName = Annotated[UNIT, Path()]

@router.get(
    "", 
    response_model=list[AllUnitsResponse],
)
def get_all_units():
    """Get all units."""
    return units_service.get_all_units()

@router.get(
    "/{unit_name}", 
    response_model=AllUnitsResponse
)
def get_unit(unit_name: UnitName):
    """Get unit by name."""
    return units_service.get_unit(unit_name)