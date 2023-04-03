from fastapi import APIRouter, Depends
from databases import Database
from schemas.schema_user import SignIn, ResponseUserSchema, UserSchema
from schemas.schema_auth import ResponseToken
from services.service_auth import get_current_user, Service_auth
from core.connections import get_db


router = APIRouter()

# sign in user
@router.post("/login", response_model=ResponseToken, status_code=200)
async def login(payload: SignIn, db: Database = Depends(get_db)) -> ResponseToken:
    token = await Service_auth(db=db).return_token(payload=payload)
    return ResponseToken(result=token, detail="success")

@router.get("/me", response_model=ResponseUserSchema, status_code=200)
async def user_info(user_response: UserSchema = Depends(get_current_user)) -> ResponseUserSchema:
    return ResponseUserSchema(result=user_response, detail="success")