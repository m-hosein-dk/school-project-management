from fastapi import APIRouter
from spm.hello_world.view import router as hello_world_router

api_router = APIRouter()

api_router.include_router(hello_world_router, prefix="/helloworld")