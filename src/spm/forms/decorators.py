from spm.units.consts import UNIT
from .models import FormMetaFunc
from . import service as forms_service

def unit_form_meta(unit: UNIT):
    def register(func: FormMetaFunc):
        forms_service.register_unit_form(unit, func)
        return func
    return register