from fastapi import APIRouter, HTTPException, status, Depends
from databases import Database
from schemas.schema_user import SignIn, ResponseUserList, UserList
from schemas.schema_auth import ResponseToken, Token
from utils.password_hasher import Hasher
from utils.user_validation import create_access_token
from services.service_auth import Service_auth, get_current_user
from services.service_user import Service_user
from core.connections import get_db


router = APIRouter()

# sign in user
@router.post("/login", response_model=ResponseToken, status_code=200)
async def login(payload: SignIn, db: Database = Depends(get_db)) -> ResponseToken:
    user = await Service_user(db=db).get_by_email(user_email=payload.user_email)
    
    # incorrect email
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email")
    
    # incorrect password
    if not Hasher.verify_password(plain_password=payload.user_password, hashed_password=user.user_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    # return token
    return ResponseToken(result=Token(
        access_token=create_access_token({"sub": user.user_email}),
        token_type="Bearer")
    )

@router.get("/me", response_model=ResponseUserList, status_code=200)
async def user_info(user_response: UserList = Depends(get_current_user)) -> ResponseUserList:
    return ResponseUserList(result=user_response)