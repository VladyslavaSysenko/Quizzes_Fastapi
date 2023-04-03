from schemas.schema_user import UserSchema
from schemas.schema_analytics import Data, ResponseData
from schemas.schema_quiz import QuizSubmitRedis
from services.service_quiz import Service_quiz
from services.service_company import Service_company
from services.service_user import Service_user
from fastapi import status, HTTPException
from fastapi.responses import StreamingResponse
from databases import Database
from pandas import DataFrame, concat
from redis.asyncio.client import Redis
from io import StringIO
import json


class Service_data:
    def __init__(self, db: Database, data_type:str, redis_db:Redis, user: UserSchema = None, company_id: int = None) -> None:
        self.db = db
        self.user = user
        self.company_id = company_id
        self.redis_db = redis_db
        self.data_type = data_type
    

    async def get_data(self, member_id:int = None, quiz_id:int = None) -> ResponseData | StreamingResponse:
        # check if user is owner or admin
        await Service_company(db=self.db, user=self.user, company_id=self.company_id).is_admin_owner()
        # check data type
        if self.data_type not in ["json", "csv"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data type can only be json or csv")
        # get json data
        # company info all users
        if not member_id and not quiz_id:
            coursor, keys = await self.redis_db.scan(coursor=0, match=f"*company_{self.company_id}*")
        # company info one user
        if member_id and not quiz_id:
            # check if user is member
            await self.is_member(member_id=member_id)
            coursor, keys = await self.redis_db.scan(coursor=0, match=f"user_{member_id}:company_{self.company_id}*")
        # quiz info
        if quiz_id:
            # check if company quiz
            await Service_quiz(db=self.db, user=self.user, company_id=self.company_id).get_quiz_by_id(quiz_id=quiz_id)
            # quiz info all users
            if not member_id:
                coursor, keys = await self.redis_db.scan(coursor=0, match=f"*company_{self.company_id}:quiz_{quiz_id}*")
            # quiz info one user    
            if member_id:
                # check if user is member
                await self.is_member(member_id=member_id)
                coursor, keys = await self.redis_db.scan(coursor=0, match=f"user_{member_id}:company_{self.company_id}:quiz_{quiz_id}*")
        values_bytes = await self.redis_db.mget(keys)
        values = [json.loads(value.decode('utf-8')) for value in values_bytes]
        # get json data
        if self.data_type == "json":
            response = ResponseData(result=Data(data=[QuizSubmitRedis(**value) for value in values]), detail="success")
        # get csv data
        if self.data_type == "csv":
            response = await self.save_csv(values=values)
        return response
    

    async def get_my_data(self, quiz_id:int = None) -> ResponseData | StreamingResponse:
        # check data type
        if self.data_type not in ["json", "csv"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data type can only be json or csv")
        if self.company_id:
            # check if user is member of this company
            if not await Service_company(db=self.db, user=self.user, company_id=self.company_id).is_member():
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a member of this company")
            # get my company data
            if not quiz_id:
                coursor, keys = await self.redis_db.scan(coursor=0, match=f"user_{self.user.user_id}:company_{self.company_id}*")
            # get my quiz data
            if quiz_id:
                # check if company quiz
                await Service_quiz(db=self.db, user=self.user, company_id=self.company_id).get_quiz_by_id(quiz_id=quiz_id)
                # return data
                coursor, keys = await self.redis_db.scan(coursor=0, match=f"user_{self.user.user_id}:company_{self.company_id}:quiz_{quiz_id}*")
        # get my all data
        else:
            coursor, keys = await self.redis_db.scan(coursor=0, match=f"user_{self.user.user_id}*")
        values_bytes = await self.redis_db.mget(keys)
        values = [json.loads(value.decode('utf-8')) for value in values_bytes]
        # get json data
        if self.data_type == "json":
            response = ResponseData(result=Data(data=[QuizSubmitRedis(**value) for value in values]), detail="success")
        # get csv data
        if self.data_type == "csv":
            response = await self.save_csv(values=values)
        return response
    
    async def save_csv(self, values:list) -> StreamingResponse:
        df = DataFrame(columns=['user_id', 'company_id', 'quiz_id', 'attempt', 'question_id', 'answer', 'is_answer_correct'])
        entry = DataFrame.from_records(values)
        df = concat([df, entry], ignore_index=True)
        stream = StringIO()
        df.to_csv(stream, index = False)
        response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=data.csv"
        return response


    async def is_member(self, member_id: int) -> None:
        user = await Service_user(db=self.db, user=self.user).get_by_id(user_id=member_id)
        if not await Service_company(db=self.db, user=user, company_id=self.company_id).is_member():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a member of this company")