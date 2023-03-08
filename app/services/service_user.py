from schemas.schema_user import SignIn, SignUp, UserList, UserUpdate, UsersList
from schemas.schema_user import User as UserSchema
from db.models import User
from utils.password_hasher import Hasher
from fastapi import HTTPException
from sqlalchemy import select, insert, delete, update
from databases import Database

class Service_user:
    
    def __init__(self, db: Database) -> None:
        self.db = db


    async def get_all(self) -> UsersList:
        query = select(User)
        users = await self.db.fetch_all(query)
        return UsersList(users=users)

    async def get_by_id(self, user_id: int) -> UserList:
        query = select(User).where(User.user_id == user_id)
        user = await self.db.fetch_one(query)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserList(**user)

    async def get_by_email(self, user_email: int) -> UserList | None:
        query = select(User).where(User.user_email == user_email)
        user = await self.db.fetch_one(query)
        if not user:
            return None
        return UserList(**user)

    async def get_by_username(self, user_username: int) -> UserList | None:
        query = select(User).where(User.user_username == user_username)
        user = await self.db.fetch_one(query)
        if not user:
            return None
        return UserList(**user)

    async def create(self, payload:SignUp) -> UserList:
        hashed_password = Hasher.get_password_hash(payload.user_password)
        query = insert(User).values(
            user_email = payload.user_email,
            user_password = hashed_password,
            user_username = payload.user_username,
            user_first_name = payload.user_first_name,
            user_last_name = payload.user_last_name
        ).returning(User)
        user = await self.db.fetch_one(query)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserList(**user)

    async def delete_user(self, user_id: int) -> dict:
        query = delete(User).where(User.user_id == user_id)
        await self.db.execute(query)
        # check if deleted
        query = select(User).where(User.user_id == user_id)
        user = await self.db.fetch_one(query)
        if user:
            raise HTTPException(status_code=500, detail="Something went wrong")
        return {"status": "successful"}

    async def update_user(self, user_id: int, payload:UserUpdate) -> UserList:
        changed_values = self.get_changed_values(payload=payload)
        query = update(User).where(User.user_id == user_id).values(
            changed_values
        ).returning(User)
        user = await self.db.fetch_one(query)
        return UserList(**user)
            
    def valid_password(self, password) -> str:
        if len(password) < 4:
            raise HTTPException(status_code=422, detail="Password must be 4+ characters long.")
        return password

    def password_repeat_match(self, password: str, password_repeat: str) -> str:
        if password != password_repeat:
            raise HTTPException(status_code=422, detail="Passwords do not match")
        return password_repeat

    def get_changed_values(self, payload:UserUpdate) -> dict:
        changed_values = {x[0]:x[1] for x in payload if x[1]}
        #hash password if changed
        if "user_password" in changed_values:
            changed_values['user_password'] = Hasher.get_password_hash(changed_values["user_password"])
            del changed_values['user_password_repeat']
        # if nothing changed
        if changed_values == {}:
            raise HTTPException(status_code=400, detail="Nothing to change")
        return changed_values