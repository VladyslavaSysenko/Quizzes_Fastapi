from schemas.schema_user import UserSchema
from schemas.schema_quiz import QuizCreate, QuizSchema, QuizzesList, QuizUpdate
from schemas.schema_quiz import QuestionCreate, QuestionUpdate, QuestionSchema, QuestionsCreate, QuestionsUpdate, QuestionsSchema
from services.service_company import Service_company
from db.models import Quiz, QuizQuestion
from fastapi import status, HTTPException
from sqlalchemy import select, insert, delete, update
from databases import Database

class Service_quiz:
    def __init__(self, db: Database, user: UserSchema = None, company_id: int = None) -> None:
        self.db = db
        self.user = user
        self.company_id = company_id


    async def get_all_quizzes(self) -> QuizzesList:
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
        if changed_question_values != []:
            await self.delete_questions(quiz_id=quiz_id)
            await self.create_questions(payload=payload.quiz_questions,quiz_id=quiz_id)
        # if quiz info changed
        if changed_quiz_values != {}:
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
        # get changed values
        changed_quiz_values = {x[0]:x[1] for x in payload if x[1] and old_quiz[x[0]] != x[1]}
        try:
            new_question_values = changed_quiz_values.get("quiz_questions")
            changed_question_values = []
            if old_questions != new_question_values:
                for question in new_question_values:
                    if question not in old_questions:
                        changed_question_values.append(question)
            del changed_quiz_values["quiz_questions"]
        except TypeError:
            changed_question_values = []
        
        # if nothing changed
        if changed_quiz_values == {} and changed_question_values == []:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nothing to change")
        return changed_quiz_values, changed_question_values