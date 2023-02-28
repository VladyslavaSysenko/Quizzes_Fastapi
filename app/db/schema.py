from pydantic import BaseModel, EmailStr


class UserList(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class User(UserList):
    password: str


class SignIn(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class SignUp(SignIn):
    username: str
    first_name: str
    last_name: str
    password_rep: str


class UserUpgrade(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None
    username: str | None = None

    class Config:
        orm_mode = True