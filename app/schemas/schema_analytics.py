from pydantic import BaseModel, validator
from datetime import date

# workflow schema
class WorkflowSchema(BaseModel):
    workflow_id: int
    workflow_user_id: int
    workflow_quiz_id: int
    workflow_company_id: int
    workflow_record_correct_answers: int
    workflow_record_all_questions: int
    workflow_record_result: float
    workflow_quiz_correct_answers: int
    workflow_quiz_all_questions: int
    workflow_quiz_result: float
    workflow_company_correct_answers: int
    workflow_company_all_questions: int
    workflow_company_result: float
    workflow_system_correct_answers: int
    workflow_system_all_questions: int
    workflow_system_result: float
    workflow_date: date

    class Config:
        orm_mode = True


# get company company users analytics for all time
class AnalyticsCompanyUsers(BaseModel):
    user_id: int
    date: date
    company_result: float

    @validator('company_result')
    def result_check(cls, v):
        return round(v, 2)

class AnalyticsCompanyCompanyUsers(BaseModel):
    company_id: int
    analytics: list[AnalyticsCompanyUsers]

class ResponseAnalyticsCompanyCompanyUsers(BaseModel):
    result: AnalyticsCompanyCompanyUsers
    detail: str


# get company company user analytics for all time
class AnalyticsCompanyUser(BaseModel):
    date: date
    company_result: float
    
    @validator('company_result')
    def result_check(cls, v):
        return round(v, 2)

class AnalyticsCompanyCompanyUser(BaseModel):
    company_id: int
    user_id: int
    analytics: list[AnalyticsCompanyUser]

class ResponseAnalyticsCompanyCompanyUser(BaseModel):
    result: AnalyticsCompanyCompanyUser
    detail: str


# get company quizzes users analytics for all time
class AnalyticsQuizzesUsers(BaseModel):
    quiz_id: int
    user_id: int
    date: date
    record_result: float
    quiz_result: float

    @validator('quiz_result', "record_result")
    def result_check(cls, v):
        return round(v, 2)

class AnalyticsCompanyQuizzesUsers(BaseModel):
    company_id: int
    analytics: list[AnalyticsQuizzesUsers]

class ResponseAnalyticsCompanyQuizzesUsers(BaseModel):
    result: AnalyticsCompanyQuizzesUsers
    detail: str


# get company quizzes user analytics for all time
class AnalyticsQuizzesUser(BaseModel):
    quiz_id: int
    date: date
    record_result: float
    quiz_result: float

    @validator('quiz_result', "record_result")
    def result_check(cls, v):
        return round(v, 2)

class AnalyticsCompanyQuizzesUser(BaseModel):
    user_id: int
    company_id: int
    analytics: list[AnalyticsQuizzesUser]

class ResponseAnalyticsCompanyQuizzesUser(BaseModel):
    result: AnalyticsCompanyQuizzesUser
    detail: str


# get company quiz users analytics for all time
class AnalyticsQuizUsers(BaseModel):
    user_id: int
    date: date
    record_result: float
    quiz_result: float

    @validator('quiz_result', "record_result")
    def result_check(cls, v):
        return round(v, 2)

class AnalyticsCompanyQuizUsers(BaseModel):
    company_id: int
    quiz_id: int
    analytics: list[AnalyticsQuizUsers]

class ResponseAnalyticsCompanyQuizUsers(BaseModel):
    result: AnalyticsCompanyQuizUsers
    detail: str


# get company quiz user analytics for all time
class AnalyticsQuizUser(BaseModel):
    date: date
    record_result: float
    quiz_result: float

    @validator('quiz_result', "record_result")
    def result_check(cls, v):
        return round(v, 2)

class AnalyticsCompanyQuizUser(BaseModel):
    user_id: int
    company_id: int
    quiz_id: int
    analytics: list[AnalyticsQuizUser]

class ResponseAnalyticsCompanyQuizUser(BaseModel):
    result: AnalyticsCompanyQuizUser
    detail: str


# get users last company record date
class AnalyticsLastRecordUsers(BaseModel):
    user_id: int
    date: date

class AnalyticsLastRecordsUsers(BaseModel):
    company_id: int
    analytics: list[AnalyticsLastRecordUsers]

class ResponseAnalyticsLastRecordsUsers(BaseModel):
    result: AnalyticsLastRecordsUsers
    detail: str


# get user system result 
class AnalyticsSystemUser(BaseModel):
    user_id: int
    system_result: float

    @validator("system_result")
    def result_check(cls, v):
        return round(v, 2)
    
class ResponseAnalyticsSystemUser(BaseModel):
    result: AnalyticsSystemUser
    detail: str


# get my companies analytics for all time
class AnalyticsMyCompanies(BaseModel):
    company_id: int
    date: date
    company_result: float
    
    @validator('company_result')
    def result_check(cls, v):
        return round(v, 2)

class ResponseAnalyticsMyCompanies(BaseModel):
    result: list[AnalyticsMyCompanies]
    detail: str


# get my quizzes analytics for all time
class AnalyticsMyQuizzes(BaseModel):
    company_id: int
    quiz_id: int
    date: date
    quiz_result: float
    
    @validator('quiz_result')
    def result_check(cls, v):
        return round(v, 2)

class ResponseAnalyticsMyQuizzes(BaseModel):
    result: list[AnalyticsMyQuizzes]
    detail: str


# get my last quizzes record date
class AnalyticsMyLastRecordQuiz(BaseModel):
    company_id: int
    quiz_id: int
    date: date

class AnalyticsMyLastRecordQuizzes(BaseModel):
    analytics: list[AnalyticsMyLastRecordQuiz]

class ResponseAnalyticsMyLastRecordQuizzes(BaseModel):
    result: AnalyticsMyLastRecordQuizzes
    detail: str


