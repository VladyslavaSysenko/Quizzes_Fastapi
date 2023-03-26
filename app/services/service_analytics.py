from schemas.schema_user import UserSchema
from schemas.schema_quiz import QuizSubmitSchema
from db.models import QuizWorkflow
from fastapi import status
from sqlalchemy import select, insert
from databases import Database
from datetime import date


class Service_analytics:
    def __init__(self, db: Database, user: UserSchema = None, company_id: int = None) -> None:
        self.db = db
        self.user = user
        self.company_id = company_id


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

        
        