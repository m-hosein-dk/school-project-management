from contextvars import ContextVar
from typing import Final
import logging
from uuid import uuid1
from sqlalchemy.orm import sessionmaker, scoped_session, create_session
from fastapi import FastAPI, Request
from .database import core
from .api import api_router
from spm.config import (
    DEFAULT_USERNAME
)
from spm.users import service as users_service

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

api = FastAPI()

# create all database tables
core.create_all()


# create default user
temp_session = create_session(core.engine)
users_service.create_default_user(temp_session)
temp_session.commit()
temp_session.close()

# @api.middleware("http")
# async def GRANT_ALL_MIDDLEWARE(request: Request, call_next):
#     request.state.user = users_service.get_user_by_username(DEFAULT_USERNAME, request.state.db) 
#     return await call_next(request)

REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[str | None] = ContextVar(REQUEST_ID_CTX_KEY, default=None)

def get_request_id() -> str | None:
    return _request_id_ctx_var.get()

@api.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request_id = str(uuid1())

    # we create a per-request id such that we can ensure that our session is scoped for a particular request.
    # see: https://github.com/tiangolo/fastapi/issues/726
    ctx_token = _request_id_ctx_var.set(request_id)
    session = None

    try:
        session = scoped_session(sessionmaker(bind=core.engine), scopefunc=get_request_id)
        request.state.db = session()

        response = await call_next(request)

        # If we got here without exceptions, commit any pending changes
        if hasattr(request.state, "db") and request.state.db.is_active:
            request.state.db.commit()

        return response

    except Exception as e:
        # Explicitly rollback on exceptions
        try:
            if hasattr(request.state, "db") and request.state.db.is_active:
                request.state.db.rollback()
        except Exception as rollback_error:
            logging.error(f"Error during rollback: {rollback_error}")

        # Re-raise the original exception
        raise e from None
    finally:
        # Always clean up resources
        if hasattr(request.state, "db"):
            # Close the session
            try:
                request.state.db.close()
                if session is not None:
                    session.remove()  # Remove the session from the registry
            except Exception as close_error:
                logging.error(f"Error closing database session: {close_error}")

        # Always reset the context variable
        _request_id_ctx_var.reset(ctx_token)

api.include_router(api_router)

app.mount("/api", api)