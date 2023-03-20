from pydantic import BaseModel, EmailStr
from datetime import datetime

# return user
class UserSchema(BaseModel):
    user_id: int
    user_username: str
    user_first_name: str | None
    user_last_name: str | None
    user_email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UsersList(BaseModel):
    users: list[UserSchema]

    class Config:
        orm_mode = True

# user
class UserSchemaFull(UserSchema):
    user_password: str

# let user in
class SignIn(BaseModel):
    user_email: EmailStr
    user_password: str

    class Config:
        orm_mode = True
        
# create user
class SignUp(SignIn):
    user_username: str
    user_first_name: str | None = None
    user_last_name: str | None = None
    user_password_repeat: str

# update user
class UserUpdate(BaseModel):
    user_first_name: str | None = None
    user_last_name: str | None = None
    user_password: str | None = None
    user_password_repeat: str | None =  None
    user_username: str | None = None

    class Config:
        orm_mode = True

# response user
class ResponseUserSchema(BaseModel):
    result: UserSchema | None
    detail: str | None

# response users
class ResponseUsersList(BaseModel):
    result: UsersList | None
    detail: str | None