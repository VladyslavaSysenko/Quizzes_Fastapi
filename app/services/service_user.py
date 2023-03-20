from schemas.schema_user import SignUp, UserSchema, UserUpdate, UsersList, UserSchemaFull
from db.models import User
from utils.password_hasher import Hasher
from fastapi import HTTPException, status
from sqlalchemy import select, insert, delete, update
from databases import Database

class Service_user:
    
    def __init__(self, db: Database, user: UserSchema = None) -> None:
        self.db = db
        self.user = user


    async def get_all(self) -> UsersList:
        query = select(User)
        users = await self.db.fetch_all(query)
        return UsersList(users=users)


    async def get_by_id(self, user_id: int) -> UserSchema:
        query = select(User).where(User.user_id == user_id)
        user = await self.db.fetch_one(query)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserSchema(**user)


    async def get_by_email(self, user_email: int) -> UserSchemaFull | None:
        query = select(User).where(User.user_email == user_email)
        user = await self.db.fetch_one(query)
        if not user:
            return None
        return UserSchemaFull(**user)


    async def create(self, payload:SignUp) -> UserSchema:
        # error if not valid passwords or do not match
        self.check_password(password=payload.user_password, password_repeat=payload.user_password_repeat)

        # error if email is registered
        db_user_by_email = await self.get_by_email(user_email=payload.user_email)
        if db_user_by_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
        # create user
        hashed_password = Hasher.get_password_hash(password=payload.user_password)
        query = insert(User).values(
            user_email = payload.user_email,
            user_password = hashed_password,
            user_username = payload.user_username,
            user_first_name = payload.user_first_name,
            user_last_name = payload.user_last_name
        ).returning(User)
        user = await self.db.fetch_one(query)
        return UserSchema(**user)


    async def delete_user(self, user_id: int) -> status:
        # check if user tries to delete itself
        self.check_id(user_id=user_id)
        # delete user
        query = delete(User).where(User.user_id == user_id)
        await self.db.execute(query)
        return status.HTTP_200_OK


    async def update_user(self, user_id: int, payload:UserUpdate) -> UserSchema:
        # check if user tries to delete itself
        self.check_id(user_id=user_id)

        # error if not valid passwords or do not match
        if payload.user_password or payload.user_password_repeat:
            self.check_password(password=payload.user_password, password_repeat=payload.user_password_repeat)
        
        # update user
        changed_values = self.get_changed_values(payload=payload)
        query = update(User).where(User.user_id == user_id).values(
            changed_values
        ).returning(User)
        user = await self.db.fetch_one(query)
        return UserSchema(**user)
            
    def check_password(self, password: str, password_repeat: str) -> str:
        if password != password_repeat:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Passwords do not match")
        if len(password) < 4:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Password must be 4+ characters long.")
        return password


    def get_changed_values(self, payload:UserUpdate) -> UserSchema:
        changed_values = {x[0]:x[1] for x in payload if x[1]}
        #hash password if changed
        if "user_password" in changed_values:
            changed_values['user_password'] = Hasher.get_password_hash(password=changed_values["user_password"])
            del changed_values['user_password_repeat']
        # if nothing changed
        if changed_values == {}:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nothing to change")
        return changed_values
    

    def check_id(self, user_id: str) -> status:
        if self.user.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your account")
        return status.HTTP_200_OK