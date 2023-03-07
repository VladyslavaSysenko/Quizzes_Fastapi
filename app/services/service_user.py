from schemas.schema_user import SignIn, SignUp, UserList, UserUpdate, UsersList
from schemas.schema_user import User as UserSchema
from db.models import User
from utils.password_hasher import Hasher
from fastapi import HTTPException
from sqlalchemy import select, insert, delete, update
from databases import Database

async def get_all(db: Database):
    query = select(User)
    return await db.fetch_all(query)

async def get_by_id(user_id: int, db: Database):
    query = select(User).where(User.user_id == user_id)
    return await db.fetch_one(query)

async def get_by_email(user_email: int, db: Database):
    query = select(User).where(User.user_email == user_email)
    return await db.fetch_one(query)

async def get_by_username(user_username: int, db: Database):
    query = select(User).where(User.user_username == user_username)
    return await db.fetch_one(query)

async def create(payload:SignUp, db: Database):
    hashed_password = Hasher.get_password_hash(payload.user_password)
    query = insert(User).values(
        user_email = payload.user_email,
        user_password = hashed_password,
        user_username = payload.user_username,
        user_first_name = payload.user_first_name,
        user_last_name = payload.user_last_name
    ).returning(User)
    return await db.fetch_one(query)

async def delete_user(user_id: int, db: Database):
    query = delete(User).where(User.user_id == user_id)
    return await db.execute(query)

async def update_user(user_id: int, payload:UserUpdate, db: Database):
    changed_values = {x[0]:x[1] for x in payload if x[1]}
    #hash password if changed
    if "user_password" in changed_values:
        changed_values['user_password'] = Hasher.get_password_hash(changed_values["user_password"])
        del changed_values['user_password_repeat']
    #update user
    query = update(User).where(User.user_id == user_id).values(
        changed_values
    ).returning(User)
    return await db.fetch_one(query)
    
async def user_exists(user_id: int, db: Database):
    user = await get_by_id(user_id, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def valid_password(password) -> str:
    if len(password) < 4:
        raise HTTPException(status_code=422, detail="Password must be 4+ characters long.")
    return password

def password_repeat_match(password: str, password_repeat: str) -> str:
    if password != password_repeat:
        raise HTTPException(status_code=422, detail="Passwords do not match")
    return password_repeat