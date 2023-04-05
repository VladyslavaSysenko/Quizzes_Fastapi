from pydantic import BaseModel, EmailStr
from schemas.schema_user import UserSchemaFull

# token
class Token(BaseModel):
    access_token: str
    token_type: str

# response token
class ResponseToken(BaseModel):
    result: Token
    detail: str

# response user by token
class ResponseUserByToken(BaseModel):
    user: UserSchemaFull
    user_email: EmailStr
    detail: str