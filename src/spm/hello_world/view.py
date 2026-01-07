from fastapi import APIRouter
from .models import (
    HelloResponse
)
from .service import get_response

router = APIRouter()

@router.get("", response_model=HelloResponse)
def hello_worlds():
    """Get all team contacts."""
    return get_response()