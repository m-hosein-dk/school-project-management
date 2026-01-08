from fastapi import APIRouter
from spm.hello_world.view import router as hello_world_router
from spm.units.views import router as units_router
from spm.users.views import router as users_router

api_router = APIRouter()

api_router.include_router(hello_world_router, prefix="/helloworld", tags=["Hello World"])
api_router.include_router(units_router, prefix="/units", tags=["Units"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])