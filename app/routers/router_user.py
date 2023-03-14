from fastapi import APIRouter, Depends
from services.service_user import Service_user
from services.service_auth import get_current_user
from schemas.schema_user import SignUp, UserList, UserUpdate, ResponseUserList, ResponseUsersList
from core.connections import get_db
from databases import Database


router =  APIRouter()


# get all users
@router.get("/users", response_model=ResponseUsersList, status_code=200)
async def get_all_users(db: Database = Depends(get_db), user: UserList = Depends(get_current_user)) -> ResponseUsersList:
    users = await Service_user(db=db).get_all()
    return ResponseUsersList(result=users)

# get user
@router.get("/user", response_model=ResponseUserList, status_code=200)
async def get_user(user_id: int, db: Database = Depends(get_db), user: UserList = Depends(get_current_user)) -> ResponseUserList:
    user = await Service_user(db=db).get_by_id(user_id=user_id)
    return ResponseUserList(result=user)

# create user
@router.post("/user", response_model=ResponseUserList, status_code=200)
async def sign_up_user(payload: SignUp, db: Database = Depends(get_db)) -> ResponseUserList:
    user = await Service_user(db=db).create(payload=payload)
    return ResponseUserList(result=user)

# update user
@router.put("/user", response_model=ResponseUserList, status_code=200)
async def update_user(user_id: int, payload: UserUpdate, db: Database = Depends(get_db), user: UserList = Depends(get_current_user)) -> ResponseUserList:
    user = await Service_user(db=db, user=user).update_user(user_id=user_id, payload=payload)
    return ResponseUserList(result=user)

# delete user
@router.delete("/user", status_code=200)
async def delete_user(user_id: int, db: Database = Depends(get_db), user: UserList = Depends(get_current_user)) -> None:
    await Service_user(db=db, user=user).delete_user(user_id=user_id)
