from fastapi import APIRouter
from .models import (
    HelloResonse
)
from .service import get_response

router = APIRouter()

@router.get("", response_model=HelloResonse)
def hello_worlds():
    """Get all team contacts."""
    return get_response()