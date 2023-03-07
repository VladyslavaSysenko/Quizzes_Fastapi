from db.models import User
from fastapi import APIRouter, Depends, HTTPException, status
from services import service_user
from schemas.schema_user import SignIn, SignUp, UserList, UserUpdate, UsersList
from schemas.schema_user import User as UserSchema
from core.connections import get_db
from databases import Database


router =  APIRouter()

# get all users
@router.get("/users", status_code=200)
async def get_all_users(db: Database = Depends(get_db)):
    users = await service_user.get_all(db)
    return {"result":UsersList(users = users)}

# get user
@router.get("/user", status_code=200)
async def get_user(user_id: int, db: Database = Depends(get_db)):
    # check if user exists
    user = await service_user.user_exists(user_id=user_id, db=db)
    return {'result':UserList(**user)}

# create user
@router.post("/user", status_code=200)
async def sign_up_user(payload: SignUp, db: Database = Depends(get_db)):
    # error if passwords are different
    service_user.password_repeat_match(payload.user_password, payload.user_password_repeat)

    # error if not valid password
    service_user.valid_password(payload.user_password)

    # error if email is registered
    db_user_by_email = await service_user.get_by_email(user_email=payload.user_email, db=db)
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # error if username exists
    db_user_by_username = await service_user.get_by_username(user_username=payload.user_username, db=db)
    if db_user_by_username:
        raise HTTPException(status_code=422, detail="Username already exists")
    
    # create user
    user = await service_user.create(payload, db=db)
    return {'result':UserList(**user)}

# update user
@router.put("/user", status_code=200)
async def update_user(user_id: int, payload: UserUpdate, db: Database = Depends(get_db)):
    # check if user exists
    user = await service_user.user_exists(user_id=user_id, db=db)
    
    # error if passwords are different
    if payload.user_password and payload.user_password_repeat:
        if payload.user_password != payload.user_password_repeat:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        
    # error if username exists
    if payload.user_username:
        db_user_by_username = await service_user.get_by_username(user_username=payload.user_username, db=db)
        if db_user_by_username and db_user_by_username.user_id != user_id:
            raise HTTPException(status_code=400, detail="Username already exists")
        
    # update user
    user = await service_user.update_user(user_id, payload, db=db)
    return {'result':UserList(**user)}

# delete user
@router.delete("/user", status_code=200)
async def delete_user(user_id: int, db: Database = Depends(get_db)):
    # check if user exists
    user = await service_user.user_exists(user_id=user_id, db=db)
    
    # delete user
    await service_user.delete_user(user_id, db=db)