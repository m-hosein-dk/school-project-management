from fastapi import Request
from spm.permissions import BasePermissions, any_permission
from spm.units.consts import UNIT
from .models import User
from .service import get_current_user

class SystemAdministrator(BasePermissions):
    def check(self, request: Request):
        current_user:User | None = get_current_user(request)
        if not current_user:
            return False

        return current_user.unit == UNIT.SYSTEM_ADMINISTRATOR

class GeneralManager(BasePermissions):
    def check(self, request: Request):
        if any_permission(
                [
                    SystemAdministrator
                ],
                request
            ):
            return True

        current_user:User | None = get_current_user(request)
        if not current_user:
            return False

        return current_user.unit == UNIT.GENERAL_MANAGER