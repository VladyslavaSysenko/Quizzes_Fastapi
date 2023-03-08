from fastapi import APIRouter, Depends, HTTPException
from services.service_user import Service_user
from schemas.schema_user import SignIn, SignUp, UserList, UserUpdate, UsersList, ResponseUserList, ResponseUsersList
from schemas.schema_user import User as UserSchema
from core.connections import get_db
from databases import Database


router =  APIRouter()

# get all users
@router.get("/users", response_model=ResponseUsersList, status_code=200)
async def get_all_users(db: Database = Depends(get_db)) -> ResponseUsersList:
    users = await Service_user(db).get_all()
    return ResponseUsersList(result=users)

# get user
@router.get("/user", response_model=ResponseUserList, status_code=200)
async def get_user(user_id: int, db: Database = Depends(get_db)) -> ResponseUserList:
    user = await Service_user(db).get_by_id(user_id=user_id)
    return ResponseUserList(result=user)

# create user
@router.post("/user", response_model=ResponseUserList, status_code=200)
async def sign_up_user(payload: SignUp, db: Database = Depends(get_db)) -> ResponseUserList:
    # error if passwords are different
    Service_user(db).password_repeat_match(payload.user_password, payload.user_password_repeat)

    # error if not valid password
    Service_user(db).valid_password(payload.user_password)

    # error if email is registered
    db_user_by_email = await Service_user(db).get_by_email(user_email=payload.user_email)
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # error if username exists
    db_user_by_username = await Service_user(db).get_by_username(user_username=payload.user_username)
    if db_user_by_username:
        raise HTTPException(status_code=422, detail="Username already exists")
    
    # create user
    user = await Service_user(db).create(payload)
    return ResponseUserList(result=user)

# update user
@router.put("/user", response_model=ResponseUserList, status_code=200)
async def update_user(user_id: int, payload: UserUpdate, db: Database = Depends(get_db)) -> ResponseUserList:
    # check if user exists
    user = await Service_user(db).get_by_id(user_id=user_id)
    
    # error if passwords are different
    if payload.user_password and payload.user_password_repeat:
        if payload.user_password != payload.user_password_repeat:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        
    # error if username exists
    if payload.user_username:
        db_user_by_username = await Service_user(db).get_by_username(user_username=payload.user_username)
        if db_user_by_username and db_user_by_username.user_id != user_id:
            raise HTTPException(status_code=400, detail="Username already exists")
        
    # update user
    user = await Service_user(db).update_user(user_id, payload)
    return ResponseUserList(result=user)

# delete user
@router.delete("/user", status_code=200)
async def delete_user(user_id: int, db: Database = Depends(get_db)) -> None:
    # check if user exists
    await Service_user(db).get_by_id(user_id=user_id)
    # delete user
    await Service_user(db).delete_user(user_id)
