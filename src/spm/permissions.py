from typing import Any
from abc import ABC, abstractmethod
from fastapi import Request
from fastapi.exceptions import HTTPException

class BasePermissions(ABC):
	bases: list["BasePermissions"] = []
	@abstractmethod
	def check(self, request: Request) -> bool: ...

class PermissionsDependency:
	def __init__(self, permissions: list[type[BasePermissions]]) -> None:
		self.permissions = permissions
	
	def check_primission(self, permission: type[BasePermissions], request:Request):
		permission_instence = permission()
		base_check = any([
			p.check(request)
			for p in permission_instence.bases
		])

		return any([permission_instence.check(request), base_check])

	def __call__(self, request:Request) -> Any:
		check_result = any([
			self.check_primission(p, request)
			for p in self.permissions
		])

		if not check_result:
			raise HTTPException(status_code=403, detail="you do not have permission to this endpoint")