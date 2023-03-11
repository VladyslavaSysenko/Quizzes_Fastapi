from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from databases import Database
from schemas.schema_user import SignIn, Token, ResponseUserList, ResponseToken, SignUp
from utils.password_hasher import Hasher, random_password
from utils.user_validation import create_access_token, decode_access_token
from services.service_user import Service_user
from core.connections import get_db


router = APIRouter()
security = HTTPBearer()

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
    return ResponseToken(result=Token(
        access_token=create_access_token({"sub": user.user_email}),
        token_type="Bearer")
    )

@router.get("/me", response_model=ResponseUserList, status_code=200)
async def user_info(credentials: str = Depends(security), db: Database = Depends(get_db)) -> ResponseUserList:
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
                user_username=None,
                user_first_name=None,
                user_last_name=None))
        user = await Service_user(db=db).get_by_email(user_email=user_email)
    return ResponseUserList(result=user)
