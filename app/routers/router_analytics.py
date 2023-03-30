from fastapi import APIRouter, Depends
from services.service_analytics import Service_analytics
from services.service_auth import get_current_user
from schemas.schema_user import UserSchema
from core.connections import get_db, get_redis
from redis.asyncio.client import Redis
from databases import Database
from schemas.schema_analytics import *


router =  APIRouter()


# get company users analytics for all time
@router.get("/analytics/company/{company_id}/members", response_model=ResponseAnalyticsCompanyCompanyUsers, status_code=200)
async def get_users_company_analytics(company_id:int, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseAnalyticsCompanyCompanyUsers:
    analytics = await Service_analytics(db=db, company_id=company_id, user=user, redis_db=redis_db).get_company_company_analytics()
    return ResponseAnalyticsCompanyCompanyUsers(result=analytics, detail="success")

# get company user analytics for all time
@router.get("/analytics/company/{company_id}/member/{member_id}", response_model=ResponseAnalyticsCompanyCompanyUser, status_code=200)
async def get_user_company_analytics(company_id:int, member_id: int, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseAnalyticsCompanyCompanyUser:
    analytics = await Service_analytics(db=db, company_id=company_id, user=user, redis_db=redis_db).get_company_company_analytics(member_id=member_id)
    return ResponseAnalyticsCompanyCompanyUser(result=analytics, detail="success")

# get company quizzes users analytics for all time
@router.get("/analytics/company/{company_id}/quizzes/members", response_model=ResponseAnalyticsCompanyQuizzesUsers, status_code=200)
async def get_users_company_quizzes_analytics(company_id:int, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseAnalyticsCompanyQuizzesUsers:
    analytics = await Service_analytics(db=db, company_id=company_id, user=user, redis_db=redis_db).get_company_quiz_analytics()
    return ResponseAnalyticsCompanyQuizzesUsers(result=analytics, detail="success")

# get company quizzes user analytics for all time
@router.get("/analytics/company/{company_id}/quizzes/member/{member_id}", response_model=ResponseAnalyticsCompanyQuizzesUser, status_code=200)
async def get_users_company_quizzes_analytics(company_id:int, member_id: int, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseAnalyticsCompanyQuizzesUser:
    analytics = await Service_analytics(db=db, company_id=company_id, user=user, redis_db=redis_db).get_company_quiz_analytics(member_id=member_id)
    return ResponseAnalyticsCompanyQuizzesUser(result=analytics, detail="success")

# get quiz users analytics for all time
@router.get("/analytics/company/{company_id}/quiz/{quiz_id}/members", response_model=ResponseAnalyticsCompanyQuizUsers, status_code=200)
async def get_users_quiz_analytics(company_id:int, quiz_id:int, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseAnalyticsCompanyQuizUsers:
    analytics = await Service_analytics(db=db, company_id=company_id, user=user, redis_db=redis_db).get_quiz_analytics(quiz_id=quiz_id)
    return ResponseAnalyticsCompanyQuizUsers(result=analytics, detail="success")

# get quiz user analytics for all time
@router.get("/analytics/company/{company_id}/quiz/{quiz_id}/member/{member_id}", response_model=ResponseAnalyticsCompanyQuizUser, status_code=200)
async def get_user_quiz_analytics(company_id:int, member_id: int, quiz_id:int, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseAnalyticsCompanyQuizUser:
    analytics = await Service_analytics(db=db, company_id=company_id, user=user, redis_db=redis_db).get_quiz_analytics(quiz_id=quiz_id, member_id=member_id)
    return ResponseAnalyticsCompanyQuizUser(result=analytics, detail="success")

# get users last company record time
@router.get("/analytics/last/company/{company_id}/members", response_model=ResponseAnalyticsLastRecordsUsers, status_code=200)
async def get_users_company_last_analytics(company_id:int, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseAnalyticsLastRecordsUsers:
    analytics = await Service_analytics(db=db, company_id=company_id, user=user, redis_db=redis_db).get_last_record()
    return ResponseAnalyticsLastRecordsUsers(result=analytics, detail="success")

# get user system result 
@router.get("/analytics/user/{user_id}", response_model=ResponseAnalyticsSystemUser, status_code=200)
async def get_user_system_result(user_id: int, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseAnalyticsSystemUser:
    analytics = await Service_analytics(db=db, user=user, redis_db=redis_db).get_user_system_analytics(user_id=user_id)
    return ResponseAnalyticsSystemUser(result=analytics, detail="success")

# get my companies analytics for all time
@router.get("/analytics/companies/my", response_model=ResponseAnalyticsMyCompanies, status_code=200)
async def get_my_companies_analytics(db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseAnalyticsMyCompanies:
    analytics = await Service_analytics(db=db, user=user, redis_db=redis_db).get_my_companies_analytics()
    return ResponseAnalyticsMyCompanies(result=analytics, detail="success")

# get my quizzes analytics for all time
@router.get("/analytics/companies/quizzes/my", response_model=ResponseAnalyticsMyQuizzes, status_code=200)
async def get_my_quizzes_analytics(db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseAnalyticsMyQuizzes:
    analytics = await Service_analytics(db=db, user=user, redis_db=redis_db).get_my_quizzes_analytics()
    return ResponseAnalyticsMyQuizzes(result=analytics, detail="success")

# get my company company analytics for all time
@router.get("/analytics/company/{company_id}/my",response_model=ResponseAnalyticsCompanyCompanyUser, status_code=200)
async def get_my_company_company_analytics(company_id:int, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseAnalyticsCompanyCompanyUser:
    analytics = await Service_analytics(db=db, company_id=company_id, user=user, redis_db=redis_db).get_company_company_analytics(my=True, member_id=user.user_id)
    return ResponseAnalyticsCompanyCompanyUser(result=analytics, detail="success")

# get my company quizzes analytics for all time
@router.get("/analytics/company/{company_id}/quizzes/my", response_model=ResponseAnalyticsCompanyQuizzesUser, status_code=200)
async def get_my_company_quizzes_analytics(company_id:int, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseAnalyticsCompanyQuizzesUser:
    analytics = await Service_analytics(db=db, company_id=company_id, user=user, redis_db=redis_db).get_company_quiz_analytics(my=True, member_id=user.user_id)
    return ResponseAnalyticsCompanyQuizzesUser(result=analytics, detail="success")

# get my quiz analytics for all time
@router.get("/analytics/company/{company_id}/quiz/{quiz_id}/my", response_model=ResponseAnalyticsCompanyQuizUser, status_code=200)
async def get_my_quiz_analytics(company_id:int, quiz_id:int, db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseAnalyticsCompanyQuizUser:
    analytics = await Service_analytics(db=db, company_id=company_id, user=user, redis_db=redis_db).get_quiz_analytics(quiz_id=quiz_id, my=True, member_id=user.user_id)
    return ResponseAnalyticsCompanyQuizUser(result=analytics, detail="success")

# get my last quizzes record time
@router.get("/analytics/last/my", response_model=ResponseAnalyticsMyLastRecordQuizzes, status_code=200)
async def get_my_last_quizzes_analytics(db: Database = Depends(get_db), redis_db:Redis = Depends(get_redis), user: UserSchema = Depends(get_current_user)) -> ResponseAnalyticsMyLastRecordQuizzes:
    analytics = await Service_analytics(db=db, user=user, redis_db=redis_db).get_last_record()
    return ResponseAnalyticsMyLastRecordQuizzes(result=analytics, detail="success")