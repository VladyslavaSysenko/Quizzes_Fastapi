from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class SignUp(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    password_rep: str

    class Config:
        orm_mode = True


class SignIn(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class UserUpgrade(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None
    username: str | None = None

    class Config:
        orm_mode = True


class UsersList(BaseModel):
    users: list[User]
    amount: int
    
    class Config:
        orm_mode = True
