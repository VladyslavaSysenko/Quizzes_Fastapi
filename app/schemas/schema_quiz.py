from pydantic import BaseModel, validator
from fastapi import status, HTTPException

# create question
class QuestionCreate(BaseModel):
    question_text: str
    question_choices: list[str]
    question_answer: str

    @validator('*', each_item=True)
    def check_str_not_empty(cls, v):
        if isinstance(v, str):
            if len(v) < 1:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="String cannot be empty")
        return v

    class Config:
        orm_mode = True

    def __hash__(self):
        return hash((self.question_text, tuple(self.question_choices), self.question_answer))

# question schema
class QuestionSchema(QuestionCreate):
    question_id: int
    question_quiz_id: int | None

    class Config:
        orm_mode = True

    def __hash__(self):
        return hash((self.question_id, self.question_quiz_id, self.question_text, tuple(self.question_choices), self.question_answer))

# update question
class QuestionUpdate(BaseModel):
    question_text: str | None
    question_choices: list[str] | None
    question_answer: str | None

    @validator('*', each_item=True)
    def check_str_not_empty(cls, v):
        if isinstance(v, str):
            if len(v) < 1:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="String cannot be empty")
        return v

    class Config:
        orm_mode = True

    def __hash__(self):
        return hash((self.question_text, tuple(self.question_choices), self.question_answer))


# create questions
class QuestionsCreate(BaseModel):
    questions: list[QuestionCreate]


# questions schema
class QuestionsSchema(BaseModel):
    questions: list[QuestionSchema]


# update questions
class QuestionsUpdate(BaseModel):
    questions: list[QuestionUpdate]

# create quiz
class QuizCreate(BaseModel):
    quiz_name: str
    quiz_description:str | None
    quiz_frequency_in_days: int
    quiz_questions: list[QuestionCreate]

    @validator('*', each_item=True)
    def check_str_not_empty(cls, v):
        if isinstance(v, str):
            if len(v) < 1:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="String cannot be empty")
        return v

    class Config:
        orm_mode = True


# quiz
class QuizSchema(BaseModel):
    quiz_id: int
    quiz_name: str
    quiz_description:str | None
    quiz_frequency_in_days: int
    quiz_questions: list | None

    def __getitem__(self, item):
        return getattr(self, item)

    def __hash__(self):
        return hash((self.quiz_id, self.quiz_name, self.quiz_description, self.quiz_frequency_in_days, tuple(self.quiz_questions)))


# update quiz
class QuizUpdate(BaseModel):
    quiz_name: str | None
    quiz_description:str | None
    quiz_frequency_in_days: int | None
    quiz_questions: list[QuestionUpdate] | None

    @validator('*', each_item=True)
    def check_str_not_empty(cls, v):
        if isinstance(v, str):
            if len(v) < 1:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="String cannot be empty")
        return v

    class Config:
        orm_mode = True


# list of quizzes
class QuizzesList(BaseModel):
    quizzes: list[QuizSchema]

    class Config:
        orm_mode = True


# response quiz
class ResponseQuizSchema(BaseModel):
    result: QuizSchema | None
    detail: str


# response quizzes
class ResponseQuizzesList(BaseModel):
    result: QuizzesList | None
    detail: str


# quiz answer form
class QuizAnswerSubmit(BaseModel):
    question_id: int
    question_answer: str


# pass the quiz
class QuizSubmit(BaseModel):
    answers: list[QuizAnswerSubmit]


# submit quiz schema
class QuizSubmitSchema(BaseModel):
    company_id: int
    quiz_id: int
    attempt: int
    all_questions: int
    correct_answers: int
    result: float


# response submit quiz
class ResponseQuizSubmitSchema(BaseModel):
    result: QuizSubmitSchema | None
    detail: str


# info for redis
class QuizSubmitRedis(BaseModel):
    user_id: int
    company_id: int
    quiz_id: int
    attempt: int
    question_id: int
    answer: str | None
    is_answer_correct: bool
