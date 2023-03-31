from schemas.schema_user import UserSchema
from schemas.schema_quiz import QuizSubmitSchema
from db.models import QuizWorkflow
from fastapi import status
from sqlalchemy import select, insert
from databases import Database
from datetime import date
from schemas.schema_user import UserSchema
from schemas.schema_analytics import *
from services.service_company import Service_company
from services.service_user import Service_user
from services.service_membership import Service_membership
import services.service_quiz as service_quiz
from fastapi import status, HTTPException
from databases import Database
from redis.asyncio.client import Redis


class Service_analytics:
    def __init__(self, db: Database, user: UserSchema = None, company_id: int = None, redis_db: Redis = None) -> None:
        self.db = db
        self.user = user
        self.company_id = company_id
        self.redis_db = redis_db


    async def record_quiz_result(self, payload: QuizSubmitSchema) -> status:
        values = {
                "workflow_user_id": self.user.user_id,
                "workflow_quiz_id": payload.quiz_id,
                "workflow_company_id": self.company_id,
                "workflow_record_correct_answers": payload.correct_answers,
                "workflow_record_all_questions": payload.all_questions,
                "workflow_record_result": payload.result,
                "workflow_date": date.today()
            }
        # quiz in system
        query = select(QuizWorkflow).where(QuizWorkflow.workflow_user_id == self.user.user_id).order_by(QuizWorkflow.workflow_id.desc()).limit(1)
        last_system_record = await self.db.fetch_one(query)
        if last_system_record:
            values.update({
                "workflow_system_correct_answers": payload.correct_answers + last_system_record.workflow_system_correct_answers,
                "workflow_system_all_questions": payload.all_questions + last_system_record.workflow_system_all_questions,
                "workflow_system_result": (payload.correct_answers + last_system_record.workflow_system_correct_answers)/
                                                (payload.all_questions + last_system_record.workflow_system_all_questions)
            })
        else:
            values.update({
                "workflow_system_correct_answers": payload.correct_answers,
                "workflow_system_all_questions": payload.all_questions,
                "workflow_system_result": payload.result
            })
        # quiz in company
        query = select(QuizWorkflow).where(QuizWorkflow.workflow_user_id == self.user.user_id,
                                           QuizWorkflow.workflow_company_id == self.company_id).order_by(QuizWorkflow.workflow_id.desc()).limit(1)
        last_company_record = await self.db.fetch_one(query)
        if last_company_record:
            values.update({
                "workflow_company_correct_answers": payload.correct_answers + last_company_record.workflow_company_correct_answers,
                "workflow_company_all_questions": payload.all_questions + last_company_record.workflow_company_all_questions,
                "workflow_company_result": (payload.correct_answers + last_company_record.workflow_company_correct_answers)/
                                                 (payload.all_questions + last_company_record.workflow_company_all_questions)
            })
        else:
            values.update({
                "workflow_company_correct_answers": payload.correct_answers,
                "workflow_company_all_questions": payload.all_questions,
                "workflow_company_result": payload.result
            })

        # quiz in quiz
        query = select(QuizWorkflow).where(QuizWorkflow.workflow_user_id == self.user.user_id,
                                           QuizWorkflow.workflow_company_id == self.company_id,
                                           QuizWorkflow.workflow_quiz_id == payload.quiz_id).order_by(QuizWorkflow.workflow_id.desc()).limit(1)
        last_quiz_record = await self.db.fetch_one(query)
        if last_quiz_record:
            values.update({
                "workflow_quiz_correct_answers": payload.correct_answers + last_quiz_record.workflow_quiz_correct_answers,
                "workflow_quiz_all_questions": payload.all_questions + last_quiz_record.workflow_quiz_all_questions,
                "workflow_quiz_result": (payload.correct_answers + last_quiz_record.workflow_quiz_correct_answers)/
                                              (payload.all_questions + last_quiz_record.workflow_quiz_all_questions)
            })
        else:
            values.update({
                "workflow_quiz_correct_answers": payload.correct_answers,
                "workflow_quiz_all_questions": payload.all_questions,
                "workflow_quiz_result": payload.result
            })
        #submit all info
        query = insert(QuizWorkflow).values(values)
        await self.db.execute(query)
        return status.HTTP_200_OK
    

    async def get_company_company_analytics(self, member_id:int = None, my: bool = False) -> AnalyticsCompanyCompanyUsers | AnalyticsCompanyCompanyUser:
        if not my:
            # check if user is owner or admin
            await Service_company(db=self.db, user=self.user, company_id=self.company_id).is_admin_owner()
        if not member_id:
            # get company users analytics for all time
            query = select(QuizWorkflow).where(QuizWorkflow.workflow_company_id == self.company_id)
            data = await self.db.fetch_all(query)
            company_analytics = [AnalyticsCompanyUsers(user_id=record.workflow_user_id, date=record.workflow_date, company_result=record.workflow_company_result) for record in data]
            company_users_analytics = AnalyticsCompanyCompanyUsers(company_id=self.company_id, analytics=company_analytics)
            return company_users_analytics

        if member_id:
        # get company user analytics for all time
            # check if user is member
            await self.is_member(member_id=member_id)
            query = select(QuizWorkflow).where(QuizWorkflow.workflow_company_id == self.company_id, QuizWorkflow.workflow_user_id == member_id)
            data = await self.db.fetch_all(query)
            company_analytics = [AnalyticsCompanyUser(date=record.workflow_date, company_result=record.workflow_company_result) for record in data]
            company_user_analytics = AnalyticsCompanyCompanyUser(company_id=self.company_id, user_id=member_id, analytics=company_analytics)
            return company_user_analytics


    async def get_company_quiz_analytics(self, member_id:int = None, my: bool = False) -> AnalyticsCompanyQuizzesUsers | AnalyticsCompanyQuizzesUser:
        if not my:
            # check if user is owner or admin
            await Service_company(db=self.db, user=self.user, company_id=self.company_id).is_admin_owner()
        if not member_id:
        # get company quizzes users analytics for all time
            query = select(QuizWorkflow).where(QuizWorkflow.workflow_company_id == self.company_id)
            data = await self.db.fetch_all(query)
            quizzes_analytics = [AnalyticsQuizzesUsers(user_id=record.workflow_user_id, quiz_id=record.workflow_quiz_id, date=record.workflow_date, 
                                                        quiz_result=record.workflow_quiz_result, record_result=record.workflow_record_result) for record in data]
            quizzes_users_analytics = AnalyticsCompanyQuizzesUsers(company_id=self.company_id, analytics=quizzes_analytics)
            return quizzes_users_analytics
        
        if member_id:
        # get company quizzes user analytics for all time
            # check if user is member
            await self.is_member(member_id=member_id)
            query = select(QuizWorkflow).where(QuizWorkflow.workflow_company_id == self.company_id, QuizWorkflow.workflow_user_id == member_id)
            data = await self.db.fetch_all(query)
            quizzes_analytics = [AnalyticsQuizzesUser(quiz_id=record.workflow_quiz_id, date=record.workflow_date, 
                                                        quiz_result=record.workflow_quiz_result, record_result=record.workflow_record_result) for record in data]
            quizzes_users_analytics = AnalyticsCompanyQuizzesUser(company_id=self.company_id, user_id=member_id, analytics=quizzes_analytics)
            return quizzes_users_analytics


    async def get_quiz_analytics(self, quiz_id:int, member_id:int = None, my: bool = False) -> AnalyticsCompanyQuizUsers | AnalyticsCompanyQuizUser:
        if not my:
            # check if user is owner or admin
            await Service_company(db=self.db, user=self.user, company_id=self.company_id).is_admin_owner()
        # check if company quiz
        await service_quiz.Service_quiz(db=self.db, company_id=self.company_id).get_quiz_by_id(quiz_id=quiz_id)
        if not member_id:
        # get quiz users analytics for all time
            query = select(QuizWorkflow).where(QuizWorkflow.workflow_company_id == self.company_id, QuizWorkflow.workflow_quiz_id == quiz_id)
            data = await self.db.fetch_all(query)
            quiz_analytics = [AnalyticsQuizUsers(user_id=record.workflow_user_id, date=record.workflow_date, quiz_result=record.workflow_quiz_result, 
                                                 record_result=record.workflow_record_result) for record in data]
            quiz_users_analytics = AnalyticsCompanyQuizUsers(company_id=self.company_id, quiz_id=quiz_id, analytics=quiz_analytics)
            return quiz_users_analytics
        if member_id:
        # get quiz user analytics for all time
            # check if user is member
            await self.is_member(member_id=member_id)
            query = select(QuizWorkflow).where(QuizWorkflow.workflow_company_id == self.company_id, QuizWorkflow.workflow_user_id == member_id, QuizWorkflow.workflow_quiz_id == quiz_id)
            data = await self.db.fetch_all(query)
            quiz_analytics = [AnalyticsQuizUser(date=record.workflow_date, quiz_result=record.workflow_quiz_result, record_result=record.workflow_record_result) for record in data]
            quiz_users_analytics = AnalyticsCompanyQuizUser(company_id=self.company_id, quiz_id=quiz_id, user_id=member_id, analytics=quiz_analytics)
            return quiz_users_analytics

    
    async def get_last_record(self) -> AnalyticsLastRecordsUsers | AnalyticsMyLastRecordQuizzes:
        # get users last company record time
        if self.company_id:
            # check if user is owner or admin
            members = await Service_membership(db=self.db, user=self.user, company_id=self.company_id).get_members()
            users_last = []
            for member in members.users:
                query = select(QuizWorkflow).where(QuizWorkflow.workflow_user_id == member.membership_user_id).order_by(QuizWorkflow.workflow_id.desc()).limit(1)
                last_record_date = (await self.db.fetch_one(query)).workflow_date
                users_last.append(AnalyticsLastRecordUsers(user_id=member.membership_user_id, date=last_record_date))
            company_last = AnalyticsLastRecordsUsers(company_id=self.company_id, analytics=users_last)
            return company_last
        else:
        # get my last quizzes record time
            query = select(QuizWorkflow).where(QuizWorkflow.workflow_user_id == self.user.user_id)
            quizzes = await self.db.fetch_all(query)
            quizzes_last = []
            for quiz in quizzes:
                query = select(QuizWorkflow).where(QuizWorkflow.workflow_user_id == self.user.user_id, 
                                                   QuizWorkflow.workflow_quiz_id == quiz.workflow_quiz_id).order_by(QuizWorkflow.workflow_id.desc()).limit(1)
                last_record_date = (await self.db.fetch_one(query)).workflow_date
                quizzes_last.append(AnalyticsMyLastRecordQuiz(company_id=quiz.workflow_company_id, quiz_id=quiz.workflow_quiz_id, date=last_record_date))
            user_last = AnalyticsMyLastRecordQuizzes(analytics=quizzes_last)
            return user_last

    
    async def get_user_system_analytics(self, user_id:int) -> AnalyticsSystemUser:
        # check if user exists
        await Service_user(db=self.db, user=self.user).get_by_id(user_id=user_id)
        query = select(QuizWorkflow).where(QuizWorkflow.workflow_user_id == user_id).order_by(QuizWorkflow.workflow_id.desc()).limit(1)
        data = await self.db.fetch_one(query)
        system_analytics = AnalyticsSystemUser(user_id=user_id, system_result=data.workflow_system_result)
        return system_analytics


    async def get_my_companies_analytics(self) -> list[AnalyticsMyCompanies]:
        query = select(QuizWorkflow).where(QuizWorkflow.workflow_user_id == self.user.user_id)
        data = await self.db.fetch_all(query)
        my_companies_analytics = [AnalyticsMyCompanies(company_id=record.workflow_company_id, date=record.workflow_date, company_result=record.workflow_company_result) for record in data]
        return my_companies_analytics
        

    async def get_my_quizzes_analytics(self) -> list[AnalyticsMyQuizzes]:
        query = select(QuizWorkflow).where(QuizWorkflow.workflow_user_id == self.user.user_id)
        data = await self.db.fetch_all(query)
        my_quizzes_analytics = [AnalyticsMyQuizzes(company_id=record.workflow_company_id, quiz_id=record.workflow_quiz_id, date=record.workflow_date, quiz_result=record.workflow_quiz_result) for record in data]
        return my_quizzes_analytics
    

    async def is_member(self, member_id: int) -> None:
        user = await Service_user(db=self.db, user=self.user).get_by_id(user_id=member_id)
        if not await Service_company(db=self.db, user=user, company_id=self.company_id).is_member():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a member of this company")