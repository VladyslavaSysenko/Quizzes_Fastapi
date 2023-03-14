from utils.user_validation import decode_access_token, create_access_token
from utils.password_hasher import Hasher
from services.service_user import Service_user
from databases import Database
from schemas.schema_auth import ResponseUserByToken, Token
from schemas.schema_user import SignUp, UserList, SignIn
from utils.password_hasher import random_password
from fastapi import Depends, status, HTTPException
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
    # create user
    if user is None:
        await Service_user(db=db).create(payload=
                SignUp(user_email=user_email,
                    user_password=random_password(),
                    user_username="User",
                    user_first_name=None,
                    user_last_name=None))
        user = await Service_user(db=db).get_by_email(user_email=user_email)
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


    # return token to user
    async def return_token(self, payload:SignIn) -> Token:
        user = await Service_user(db=self.db).get_by_email(user_email=payload.user_email)
    
        # incorrect email
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email")
        
        # incorrect password
        if not Hasher.verify_password(plain_password=payload.user_password, hashed_password=user.user_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        return Token(access_token=create_access_token({"sub": user.user_email}), token_type="Bearer")