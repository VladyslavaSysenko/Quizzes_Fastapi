from pydantic import BaseModel, EmailStr
from schemas.schema_user import UserSchema

# token
class Token(BaseModel):
    access_token: str
    token_type: str

# response token
class ResponseToken(BaseModel):
    result: Token

# response user by token
class ResponseUserByToken(BaseModel):
    user: UserSchema
    user_email: EmailStr