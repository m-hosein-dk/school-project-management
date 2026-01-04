from .models import (
    HelloResonse
)

def get_response():
    return HelloResonse(hello="world")