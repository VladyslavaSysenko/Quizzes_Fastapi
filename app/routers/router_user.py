from fastapi import APIRouter, Depends, HTTPException, status
from services.service_user import Service_user
from services.service_auth import get_current_user
from schemas.schema_user import SignIn, SignUp, UserList, UserUpdate, UsersList, ResponseUserList, ResponseUsersList
from schemas.schema_user import User as UserSchema
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
    # error if passwords are different
    Service_user(db=db).password_repeat_match(password=payload.user_password, password_repeat=payload.user_password_repeat)

    # error if not valid password
    Service_user(db=db).valid_password(password=payload.user_password)

    # error if email is registered
    db_user_by_email = await Service_user(db=db).get_by_email(user_email=payload.user_email)
    if db_user_by_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # create user
    user = await Service_user(db=db).create(payload=payload)
    return ResponseUserList(result=user)

# update user
@router.put("/user", response_model=ResponseUserList, status_code=200)
async def update_user(user_id: int, payload: UserUpdate, db: Database = Depends(get_db), user: UserList = Depends(get_current_user)) -> ResponseUserList:
    # check if user tries to delete itself
    Service_user(db=db).check_id(user=user, user_id=user_id)
    
    # error if passwords are different
    if payload.user_password and payload.user_password_repeat:
        if payload.user_password != payload.user_password_repeat:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
        
    # update user
    user = await Service_user(db=db).update_user(user_id=user_id, payload=payload)
    return ResponseUserList(result=user)

# delete user
@router.delete("/user", status_code=200)
async def delete_user(user_id: int, db: Database = Depends(get_db), user: UserList = Depends(get_current_user)) -> None:
    # check if user tries to delete itself
    Service_user(db=db).check_id(user=user, user_id=user_id)
    
    # delete user
    await Service_user(db=db).delete_user(user_id=user_id)
