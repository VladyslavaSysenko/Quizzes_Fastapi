from core.connections import get_db
from databases import Database
from db.models import Notification, QuizWorkflow
from sqlalchemy import select, insert
from services.service_quiz import Service_quiz
from services.service_company import Service_company
from datetime import date, timedelta
from schemas.schema_membership import MembershipSchema
from schemas.schema_company import CompanySchema
from apscheduler.schedulers.asyncio import AsyncIOScheduler


def start_scheduler() -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_all_notifications, "cron", hour=3, minute=0)
    scheduler.start()


async def send_all_notifications() -> None:
    # send notification to all users if they can take a quiz
    db = get_db()
    companies = (await Service_company(db=db).get_all()).companies
    if companies != []:
        for company in companies:
            members = (await Service_company(db=db, company_id=company.company_id).get_members()).users
            quizzes = (await Service_quiz(db=db, company_id=company.company_id).get_all_quizzes(scheduler=True)).quizzes
            if quizzes != [] and members != []:
                for quiz in quizzes:
                    for member in members:
                        query = select(QuizWorkflow).where(QuizWorkflow.workflow_quiz_id == quiz.quiz_id, 
                                                        QuizWorkflow.workflow_user_id == member.membership_user_id).order_by(QuizWorkflow.workflow_id.desc()).limit(1)
                        last_record = await db.fetch_one(query)
                        if not last_record:
                            await send_notification(user_id=member.membership_user_id, quiz=quiz, company=company, db=db)
                        else:
                            if (last_record.workflow_date - date.today()) >= timedelta(days=quiz.quiz_frequency_in_days):
                                await send_notification(user_id=member.membership_user_id, quiz=quiz, company_id=company.company_id, db=db)
                        

async def send_notification(user_id:int, quiz:MembershipSchema, company:CompanySchema, db:Database) -> None:
    query = insert(Notification).values(
                    notification_user_id = user_id,
                    notification_quiz_id = quiz.quiz_id,
                    notification_company_id = company.company_id,
                    notification_status = False,
                    notification_text = f'Quiz №{quiz.quiz_id} "{quiz.quiz_name}" is available to take in company "{company.company_name}"'
                )
    await db.execute(query)

                



