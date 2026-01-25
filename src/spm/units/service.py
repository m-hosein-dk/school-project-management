from .consts import UNIT, language_mapping
from .models import UnitIn, UnitResponse

def get_units_language_mapping(unit:UnitIn):
    return language_mapping[unit.name]

def get_unit(unit: UNIT):
    return UnitResponse(
        name=unit,
        language_mapping=language_mapping[unit]
    )

def get_all_units() -> list[UnitResponse]:
    return [UnitResponse(name=unit, language_mapping=language_mapping[unit]) for unit in UNIT]