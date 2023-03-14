from fastapi import APIRouter, Depends
from databases import Database
from schemas.schema_user import SignIn, ResponseUserList, UserList
from schemas.schema_auth import ResponseToken
from services.service_auth import get_current_user, Service_auth
from core.connections import get_db


router = APIRouter()

# sign in user
@router.post("/login", response_model=ResponseToken, status_code=200)
async def login(payload: SignIn, db: Database = Depends(get_db)) -> ResponseToken:
    token = await Service_auth(db=db).return_token(payload=payload)
    return ResponseToken(result=token)

@router.get("/me", response_model=ResponseUserList, status_code=200)
async def user_info(user_response: UserList = Depends(get_current_user)) -> ResponseUserList:
    return ResponseUserList(result=user_response)