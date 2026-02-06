from spm.units.consts import UNIT
from .models import ProjectConstrainMetaFunc
from . import service as projects_service

def project_constain_meta(unit: UNIT):
    def register(func: ProjectConstrainMetaFunc):
        projects_service.register_project_constrain_meta(unit, func)
        return func
    return register