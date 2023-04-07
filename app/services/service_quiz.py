from schemas.schema_user import UserSchema
from schemas.schema_quiz import QuizCreate, QuizSchema, QuizzesList, QuizUpdate, QuizSubmit, QuizSubmitSchema, QuizSubmitRedis
from schemas.schema_quiz import QuestionUpdate, QuestionsCreate, QuestionsSchema
from services.service_company import Service_company
import services.service_analytics as service_analytics
from services.service_membership import Service_membership
from db.models import Quiz, QuizQuestion, QuizWorkflow, Notification
from fastapi import status, HTTPException
from sqlalchemy import select, insert, delete, update
from databases import Database
from datetime import date, timedelta
import json

class Service_quiz:
    def __init__(self, db: Database, user: UserSchema = None, company_id: int = None) -> None:
        self.db = db
        self.user = user
        self.company_id = company_id


    async def get_all_quizzes(self, scheduler:bool = False) -> QuizzesList:
        if not scheduler:
            # check if user is member
            if not await Service_company(db=self.db, user=self.user, company_id=self.company_id).is_member():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not a member of this company")
        query = select(Quiz).where(Quiz.quiz_company_id == self.company_id)
        quizzes = await self.db.fetch_all(query)
        quizzes_with_questions = []
        for quiz in quizzes:
            quiz_questions = await self.get_questions_by_quiz_id(quiz_id=quiz.quiz_id)
            quizzes_with_questions.append(QuizSchema(**quiz, quiz_questions=quiz_questions.questions))
        return QuizzesList(quizzes=quizzes_with_questions)


    async def get_quiz_by_id(self, quiz_id:str) -> QuizSchema:
        query = select(Quiz).where(Quiz.quiz_id == quiz_id)
        quiz = await self.db.fetch_one(query)
        if not quiz:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
        if quiz.quiz_company_id != self.company_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your company's quiz")
        
        quiz_questions = await self.get_questions_by_quiz_id(quiz_id=quiz_id)
        return QuizSchema(**quiz, quiz_questions=quiz_questions.questions)


    async def get_questions_by_quiz_id(self, quiz_id:int) -> QuestionsSchema:
        query = select(QuizQuestion).where(QuizQuestion.question_quiz_id == quiz_id)
        quiz_questions = await self.db.fetch_all(query)
        return QuestionsSchema(questions=quiz_questions)


    async def submit_quiz(self, quiz_id:int, payload:QuizSubmit, redis_db) -> QuizSubmitSchema:
        # check if user is member
        if not await Service_company(db=self.db, user=self.user, company_id=self.company_id).is_member():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a member of this company")
        # check if company quiz
        quiz = (await self.get_quiz_by_id(quiz_id=quiz_id))
        quiz_questions = quiz.quiz_questions
        # check if no duplicates in quiz question ids
        id_answered_questions = [record.question_id for record in payload.answers]
        if len(id_answered_questions) != len(set(id_answered_questions)):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Question ids cannot be duplicated")
        # check if quiz questions
        id_quiz_questions = {question.question_id for question in quiz_questions}
        extra_ids = set(id_answered_questions).difference(id_quiz_questions)
        if extra_ids:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Quiz does not contain question(s) with id {', '.join(str(id) for id in extra_ids)}")
        # check if user can submit quiz
        frequency = quiz.quiz_frequency_in_days
        query = select(QuizWorkflow).where(QuizWorkflow.workflow_quiz_id == quiz_id, 
                                           QuizWorkflow.workflow_user_id == self.user.user_id).order_by(QuizWorkflow.workflow_id.desc())
        records_reverse = await self.db.fetch_all(query)
        if records_reverse:
            records_amount = len(records_reverse)
            difference = records_reverse[0].workflow_date - date.today()
            if difference <  timedelta(days=frequency):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You must wait {timedelta(days=frequency).days - difference.days} more day(s)")
        else:
            records_amount = 0
        # check answers and save them in redis for 2 days
        correct_answers = 0
        all_questions = len(quiz_questions)
        not_answered_questions = id_quiz_questions.difference(set(id_answered_questions))
        for question in quiz_questions:
            # save false in redis if no answer
            if question.question_id in not_answered_questions:
                redis_user_results = QuizSubmitRedis(user_id=self.user.user_id, company_id=self.company_id, quiz_id=quiz_id, attempt=records_amount+1, question_id=question.question_id, answer=None, is_answer_correct=False)
                await redis_db.set(f"user_{self.user.user_id}:company_{self.company_id}:quiz_{quiz_id}:question_{question.question_id}:attempt_{records_amount+1}", json.dumps(dict(redis_user_results)), ex=172800)
                break
            else:
                for record in payload.answers:
                    # check answer
                    if question.question_id == record.question_id:
                        redis_user_results = QuizSubmitRedis(user_id=self.user.user_id, company_id=self.company_id, quiz_id=quiz_id, attempt=records_amount+1, 
                                                            question_id=question.question_id, answer=record.question_answer, is_answer_correct=False)
                        if record.question_answer == question.question_answer:
                            correct_answers+=1
                            redis_user_results.is_answer_correct = True
                        await redis_db.set(f"user_{self.user.user_id}:company_{self.company_id}:quiz_{quiz_id}:question_{question.question_id}:attempt_{records_amount+1}", json.dumps(dict(redis_user_results)), ex=172800)
                        break
        result = correct_answers/all_questions
        total = QuizSubmitSchema(company_id=self.company_id, quiz_id=quiz_id, attempt=records_amount+1, all_questions=all_questions, correct_answers=correct_answers, result=result)
        # create workflow analytics
        await service_analytics.Service_analytics(db=self.db, user=self.user, company_id=self.company_id).record_quiz_result(payload=total)
        return total


    async def create_quiz(self, payload:QuizCreate) -> QuizSchema:
        # check if user is owner or admin
        await Service_company(db=self.db, user=self.user, company_id=self.company_id).is_admin_owner()
        # check if questions are valid
        await self.check_questions(questions=payload.quiz_questions)
        # create quiz
        query = insert(Quiz).values(
            quiz_name = payload.quiz_name,
            quiz_description = payload.quiz_description,
            quiz_frequency_in_days = payload.quiz_frequency_in_days, 
            quiz_company_id = self.company_id
        )
        quiz_id = await self.db.execute(query)
        # create quiz questions
        await self.create_questions(payload=payload.quiz_questions, quiz_id=quiz_id)
        # add questions to quiz
        quiz = await self.get_quiz_by_id(quiz_id=quiz_id)
        # send notification to all company users except creator
        members = (await Service_membership(db=self.db, company_id=self.company_id).get_members()).users
        for member in members:
            if member.membership_user_id != self.user.user_id:
                query = insert(Notification).values(
                    notification_user_id = member.membership_user_id,
                    notification_quiz_id = quiz_id,
                    notification_company_id = self.company_id,
                    notification_status = False,
                    notification_text = f'New quiz "{payload.quiz_name}" №{quiz.quiz_id} has been created'
                )
                await self.db.execute(query)
        return quiz


    async def create_questions(self, payload:QuestionsCreate, quiz_id:int) -> status:
        questions = []
        for question in payload:
            question = {
             "question_text": question.question_text,
             "question_choices": question.question_choices,
             "question_answer": question.question_answer,
             "question_quiz_id": quiz_id
            }
            questions.append(question)
        await self.db.execute_many(query=insert(QuizQuestion), values=questions)
        return status.HTTP_200_OK


    async def check_questions(self, questions:QuestionsCreate) -> status:
        # check if at least two questions
        if len(questions) < 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz must have at least two questions")
        # check if questions are different
        if len(questions) != len(set(questions)):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Questions must be different")
        # check questions
        for question in questions:
            # check if at least two choices in questions
            if len(question.question_choices) < 2:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Question must have at least two answer choices")
            # check if choices are different:
            if len(question.question_choices) != len(set(question.question_choices)):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Answer choices must be different")
            # check if answer is in choices
            if question.question_answer not in question.question_choices:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Correct answer must be in answer choices")
        return status.HTTP_200_OK


    async def update_quiz(self, payload:QuizUpdate, quiz_id:int) -> QuizSchema:
        # check if user is owner or admin
        await Service_company(db=self.db, user=self.user, company_id=self.company_id).is_admin_owner()
        # check if quiz in company
        old_quiz = await self.get_quiz_by_id(quiz_id=quiz_id)
        # check if questions are valid
        try:
            await self.check_questions(questions=payload.quiz_questions)
        except TypeError:
            pass
        # find out what changed
        changed_quiz_values, changed_question_values = await self.get_changed_values(payload=payload, old_quiz=old_quiz)
        # if questions changed
        if changed_question_values:
            await self.delete_questions(quiz_id=quiz_id)
            await self.create_questions(payload=payload.quiz_questions,quiz_id=quiz_id)
        # if quiz info changed
        if changed_quiz_values:
            query=update(Quiz).where(Quiz.quiz_id == quiz_id).values(
                changed_quiz_values
            )
            await self.db.execute(query)
        quiz = await self.get_quiz_by_id(quiz_id=quiz_id)
        return quiz
    

    async def delete_quiz(self, quiz_id:int) -> status:
        # check if user is owner or admin
        await Service_company(db=self.db, user=self.user, company_id=self.company_id).is_admin_owner()
        # check if quiz exists
        await self.get_quiz_by_id(quiz_id=quiz_id)
        # delete quiz
        query = delete(Quiz).where(Quiz.quiz_id == quiz_id)
        await self.db.execute(query)
        return status.HTTP_200_OK
    

    async def delete_questions(self, quiz_id:int) -> status:
        query = delete(QuizQuestion).where(QuizQuestion.question_quiz_id == quiz_id)
        await self.db.execute(query)
        return status.HTTP_200_OK


    async def get_changed_values(self, payload:QuizUpdate, old_quiz:QuizSchema) -> tuple():
        old_questions=[QuestionUpdate(**question.dict()) for question in old_quiz.quiz_questions]
        # get changed quiz values
        changed_quiz_values = {x[0]:x[1] for x in payload if x[1] and old_quiz[x[0]] != x[1]}
        # get changed question values
        new_question_values = changed_quiz_values.get("quiz_questions")
        changed_question_values = []
        if new_question_values:
            if old_questions != new_question_values:
                for question in new_question_values:
                    if question not in old_questions:
                        changed_question_values.append(question)
            del changed_quiz_values["quiz_questions"]
        # if nothing changed
        if not changed_quiz_values and not changed_question_values:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nothing to change")
        return changed_quiz_values, changed_question_values