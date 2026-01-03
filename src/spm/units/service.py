from .consts import UNIT, language_mapping
from .models import UnitIn, UnitOut

def get_units_language_mapping(unit:UnitIn):
    return language_mapping[unit.name]

def get_unit(unit: UNIT):
    return UnitOut(
        name=unit,
        language_mapping=language_mapping[unit]
    )

def get_all_units() -> list[UnitOut]:
    return [UnitOut(name=unit, language_mapping=language_mapping[unit]) for unit in UNIT]