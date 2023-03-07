from pydantic import BaseModel, EmailStr

# return user
class UserList(BaseModel):
    user_id: int | None = None
    user_username: str | None = None
    user_first_name: str | None = None
    user_last_name: str | None = None
    user_email: EmailStr | None = None

    class Config:
        orm_mode = True

class UsersList(BaseModel):
    users: list[UserList]
    class Config:
        orm_mode = True

# user
class User(UserList):
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
    user_first_name: str
    user_last_name: str
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