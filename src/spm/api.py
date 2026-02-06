from fastapi import APIRouter
from spm.hello_world.view import router as hello_world_router
from spm.units.views import router as units_router
from spm.users.views import router as users_router
from spm.auth.views import router as auth_router
from spm.forms.views import router as forms_router
from spm.projects.views import router as projects_router
from spm.files.views import router as files_router

api_router = APIRouter()

api_router.include_router(hello_world_router, prefix="/helloworld", tags=["Hello World"])
api_router.include_router(units_router, prefix="/units", tags=["Units"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(forms_router, prefix="/forms", tags=["Forms"])
api_router.include_router(projects_router, prefix="/projects", tags=["Projects"])
api_router.include_router(files_router, prefix="/files", tags=["Files"])