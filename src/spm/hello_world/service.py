from .models import (
    TestResponse
)

def get_response():
    return TestResponse(hello="world")