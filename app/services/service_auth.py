from utils.user_validation import create_access_token, decode_access_token
from services.service_user import Service_user
from databases import Database
from schemas.schema_auth import ResponseUserByToken
from schemas.schema_user import SignUp, UserList
from schemas.schema_user import User as UserSchema
from utils.password_hasher import random_password
from pydantic import EmailStr
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from core.connections import get_db

security = HTTPBearer()

# get authorized user by token
async def get_current_user(db:Database = Depends(get_db), credentials: str = Depends(security)) -> UserList:
    decoded_token = decode_access_token(token=credentials.credentials)
    try:
        user_email = decoded_token["email"]
    except:
        user_email = decoded_token["sub"]
    user = await Service_user(db=db).get_by_email(user_email=user_email)
    # error not authorized
    if user is None:
        user = await Service_auth(db=db).create_user_by_email(user_email=user_email)
    return UserList(**user.dict())

class Service_auth:

    def __init__(self, db: Database) -> None:
        self.db = db

    # get user and email by token
    async def get_user_by_token(self, credentials: str) -> ResponseUserByToken:
        decoded_token = decode_access_token(token=credentials.credentials)
        try:
            user_email = decoded_token["email"]
        except:
            user_email = decoded_token["sub"]
        user = await Service_user(db=self.db).get_by_email(user_email=user_email)
        return ResponseUserByToken(user=user, user_email=user_email)

    # create user by token
    async def create_user_by_email(self, user_email: EmailStr) -> UserSchema:
        await Service_user(db=self.db).create(payload=
                SignUp(user_email=user_email,
                    user_password=random_password(),
                    user_username="User",
                    user_first_name=None,
                    user_last_name=None))
        user = await Service_user(db=self.db).get_by_email(user_email=user_email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
        return user