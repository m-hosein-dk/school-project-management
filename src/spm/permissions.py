from typing import Any
from abc import ABC, abstractmethod
from fastapi import Request
from fastapi.exceptions import HTTPException

def any_permission(permissions: list[type["BasePermissions"]], request:Request) -> bool:
	for permission in permissions:
		if permission().check(request):
			return True
	return False

class BasePermissions(ABC):
	@abstractmethod
	def check(self, request: Request) -> bool: ...

class PermissionsDependency:
	def __init__(self, permissions: list[type[BasePermissions]]) -> None:
		self.permissions = permissions

	def __call__(self, request:Request) -> Any:
		check_result = any([
			p().check(request)
			for p in self.permissions
		])

		if not check_result:
			raise HTTPException(status_code=403, detail="you do not have permission to this endpoint")