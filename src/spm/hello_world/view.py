from fastapi import APIRouter, Request
from .models import (
    TestResponse
)
from .service import get_response

router = APIRouter()

@router.get("", response_model=TestResponse)
def hello_worlds(request:Request):
    """Get all team contacts."""
    return get_response()