from typing import Annotated
import logging
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status, Request, Header
from spm.core import DbSession
from spm.users.models import (
	User
)
from spm.users import service as users_service
from .models import (
	ChangePassword,
	UsernamePasswordLogin,
	AccessToken
)
from .utils import (
	gen_jwt_for_user,
	get_id_from_jwt,
	authorization_params
)

log = logging.getLogger(__name__)

def username_password_login(
		credentials: UsernamePasswordLogin, 
		session:Session
	) -> AccessToken:
	user = users_service.get_user_by_username(credentials.username, session)

	if user:
		if user.verify_password(credentials.password):
			access_token = AccessToken(
				type = "Bearer",
				token = gen_jwt_for_user(user)
			)

			return access_token
	
	raise HTTPException(
		status.HTTP_403_FORBIDDEN,
		detail="Invalid username or password"
	)

def user_from_header(
	header: str | None, 
	session:Session
):
	if not header:
		return None

	type, token = authorization_params(header)

	if type.lower() != "bearer":
		raise HTTPException(
			status.HTTP_401_UNAUTHORIZED,
			detail="invalid token type"
		)
	if not token:
		raise HTTPException(
			status.HTTP_401_UNAUTHORIZED,
			detail="invalid"
		)
	
	user_id = get_id_from_jwt(token)

	log.info(f'got {user_id} from auth token')

	user = users_service.get_user(user_id, session)

	if not user:
		raise HTTPException(
			status.HTTP_401_UNAUTHORIZED
		)
	
	return user

def auth_dependency(
	session: DbSession,
	request: Request,
	header: Annotated[str | None, Header(alias="Authorization")] = None,
):
	request.state.user = user_from_header(header, session)

def change_password(
	model: ChangePassword,
	user: User,
):
	if user.password:
		if not user.verify_password(model.old_password):
			raise HTTPException(
				status.HTTP_403_FORBIDDEN,
				detail="old password wrong"
			)

	user.set_password(model.new_password)