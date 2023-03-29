from fastapi import APIRouter, Depends
from services.service_data import Service_data
from services.service_auth import get_current_user
from schemas.schema_user import UserSchema
from schemas.schema_data import ResponseData
from core.connections import get_db, get_redis
from databases import Database
from redis.asyncio.client import Redis
from starlette.responses import StreamingResponse


router =  APIRouter()


# get all users company info
@router.get("/data/{data_type}/company/{company_id}/quizzes", response_model=ResponseData, status_code=200)
async def get_users_company_data(company_id:int, data_type:str, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseData | StreamingResponse:
    data = await Service_data(db=db, company_id=company_id, user=user, redis_db=redis_db, data_type=data_type).get_data()
    return data

# get one user company info
@router.get("/data/{data_type}/company/{company_id}/quizzes/member/{member_id}", response_model=ResponseData, status_code=200)
async def get_user_company_data(company_id:int, data_type:str, member_id: int, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseData | StreamingResponse:
    data = await Service_data(db=db, company_id=company_id, user=user, redis_db=redis_db, data_type=data_type).get_data(member_id=member_id)
    return data

# get all users quiz info
@router.get("/data/{data_type}/company/{company_id}/quiz/{quiz_id}", response_model=ResponseData, status_code=200)
async def get_users_quiz_data(company_id:int, data_type:str, quiz_id:int, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseData | StreamingResponse:
    data = await Service_data(db=db, company_id=company_id, user=user, redis_db=redis_db, data_type=data_type).get_data(quiz_id=quiz_id)
    return data

# get one user quiz info 
@router.get("/data/{data_type}/company/{company_id}/quiz/{quiz_id}/member/{member_id}", response_model=ResponseData, status_code=200)
async def get_user_quiz_data(company_id:int, data_type:str, member_id: int, quiz_id:int, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseData | StreamingResponse:
    data = await Service_data(db=db, company_id=company_id, user=user, redis_db=redis_db, data_type=data_type).get_data(quiz_id=quiz_id, member_id=member_id)
    return data

# get my all data
@router.get("/data/{data_type}/my", response_model=ResponseData, status_code=200)
async def get_my_data(data_type:str, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseData | StreamingResponse:
    data = await Service_data(db=db, user=user, redis_db=redis_db, data_type=data_type).get_my_data()
    return data

#get my company data
@router.get("/data/{data_type}/company/{company_id}/my", response_model=ResponseData, status_code=200)
async def get_my_data(company_id:int, data_type:str, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseData | StreamingResponse:
    data = await Service_data(db=db, user=user, company_id=company_id, redis_db=redis_db, data_type=data_type).get_my_data()
    return data

#get my quiz data
@router.get("/data/{data_type}/company/{company_id}/quiz/{quiz_id}/my", response_model=ResponseData, status_code=200)
async def get_my_data(company_id:int, data_type:str, quiz_id:int, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseData | StreamingResponse:
    data = await Service_data(db=db, user=user, company_id=company_id, redis_db=redis_db, data_type=data_type).get_my_data(quiz_id=quiz_id)
    return data