from fastapi import APIRouter, Depends
from services.service_user import Service_user
from services.service_auth import get_current_user
from schemas.schema_user import SignUp, UserSchema, UserUpdate, ResponseUserSchema, ResponseUsersList
from core.connections import get_db
from databases import Database


router =  APIRouter()


# get all users
@router.get("/users", response_model=ResponseUsersList, status_code=200)
async def get_all_users(db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseUsersList:
    users = await Service_user(db=db).get_all()
    return ResponseUsersList(result=users)

# get user
@router.get("/user/{user_id}", response_model=ResponseUserSchema, status_code=200)
async def get_user(user_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseUserSchema:
    user = await Service_user(db=db).get_by_id(user_id=user_id)
    return ResponseUserSchema(result=user)

# create user
@router.post("/user", response_model=ResponseUserSchema, status_code=200)
async def sign_up_user(payload: SignUp, db: Database = Depends(get_db)) -> ResponseUserSchema:
    user = await Service_user(db=db).create(payload=payload)
    return ResponseUserSchema(result=user)

# update user
@router.put("/user/{user_id}", response_model=ResponseUserSchema, status_code=200)
async def update_user(user_id: int, payload: UserUpdate, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseUserSchema:
    user = await Service_user(db=db, user=user).update_user(user_id=user_id, payload=payload)
    return ResponseUserSchema(result=user)

# delete user
@router.delete("/user/{user_id}", status_code=200)
async def delete_user(user_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> None:
    await Service_user(db=db, user=user).delete_user(user_id=user_id)
