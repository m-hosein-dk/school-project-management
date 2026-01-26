from pydantic import BaseModel

# pydantic models...
class UsernamePasswordLogin(BaseModel):
    username:str
    password:str

class AccessToken(BaseModel):
    type: str # Bearer
    token: str

class ChangePassword(BaseModel):
    old_password:str
    new_password:str

# class JwtPayload(BaseModel):
#     user_id: int