from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, Request


def get_db(request: Request) -> Session:
    """Get database session from request state."""
    session = request.state.db
    return session


DbSession = Annotated[Session, Depends(get_db)]