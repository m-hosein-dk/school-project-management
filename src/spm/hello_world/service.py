from datetime import datetime
from sqlalchemy.orm import Session
from .models import (
    HelloResponse
)

def get_response():
    return HelloResponse(hello="world")