from pydantic import BaseModel, validator
from datetime import date
from schemas.schema_quiz import QuizSubmitRedis


# get redis data
class Data(BaseModel):
    data: list[QuizSubmitRedis]

class ResponseData(BaseModel):
    result: Data
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


# get company company users analytics for all time
class AnalyticsCompanyUsers(BaseModel):
    user_id: int
    analytics: list[AnalyticsCompanyUser]

class AnalyticsCompanyCompanyUsers(BaseModel):
    company_id: int
    analytics: list[AnalyticsCompanyUsers]

class ResponseAnalyticsCompanyCompanyUsers(BaseModel):
    result: AnalyticsCompanyCompanyUsers
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
    company_id: int
    quiz_id: int
    user_id: int
    analytics: list[AnalyticsQuizUser]

class ResponseAnalyticsCompanyQuizUser(BaseModel):
    result: AnalyticsCompanyQuizUser
    detail: str


# get company quizzes user analytics for all time
class AnalyticsQuizzesUser(BaseModel):
    quiz_id: int
    analytics: list[AnalyticsQuizUser]

class AnalyticsCompanyQuizzesUser(BaseModel):
    company_id: int
    user_id: int
    analytics: list[AnalyticsQuizzesUser]

class ResponseAnalyticsCompanyQuizzesUser(BaseModel):
    result: AnalyticsCompanyQuizzesUser
    detail: str


# get company quiz users analytics for all time
class AnalyticsQuizUsers(BaseModel):
    user_id: int
    analytics: list[AnalyticsQuizUser]

class AnalyticsCompanyQuizUsers(BaseModel):
    company_id: int
    quiz_id: int
    analytics: list[AnalyticsQuizUsers]

class ResponseAnalyticsCompanyQuizUsers(BaseModel):
    result: AnalyticsCompanyQuizUsers
    detail: str


# get company quizzes users analytics for all time
class AnalyticsQuizzesUsers(BaseModel):
    quiz_id: int
    analytics: list[AnalyticsQuizUsers]

class AnalyticsCompanyQuizzesUsers(BaseModel):
    company_id: int
    analytics: list[AnalyticsQuizzesUsers]

class ResponseAnalyticsCompanyQuizzesUsers(BaseModel):
    result: AnalyticsCompanyQuizzesUsers
    detail: str


# get users last company record date
class AnalyticsLastRecordUsers(BaseModel):
    user_id: int
    date: date | None

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
class AnalyticsMyCompany(BaseModel):
    date: date
    company_result: float
    
    @validator('company_result')
    def result_check(cls, v):
        return round(v, 2)

class AnalyticsMyCompanies(BaseModel):
    company_id: int
    analytics: list[AnalyticsMyCompany]

class ResponseAnalyticsMyCompanies(BaseModel):
    result: list[AnalyticsMyCompanies]
    detail: str


# get my quizzes analytics for all time
class AnalyticsMyCompanyQuiz(BaseModel):
    date: date
    quiz_result: float
    
    @validator('quiz_result')
    def result_check(cls, v):
        return round(v, 2)

class AnalyticsMyCompanyQuizzes(BaseModel):
    quiz_id: int
    analytics: list[AnalyticsMyCompanyQuiz]

class AnalyticsMyCompaniesQuizzes(BaseModel):
    company_id: int
    analytics: list[AnalyticsMyCompanyQuizzes]

class ResponseAnalyticsMyQuizzes(BaseModel):
    result: list[AnalyticsMyCompaniesQuizzes]
    detail: str


# get my last quizzes record date
class AnalyticsMyLastRecordQuiz(BaseModel):
    quiz_id: int
    date: date

class AnalyticsMyLastRecordQuizzes(BaseModel):
    company_id: int
    last_records: list[AnalyticsMyLastRecordQuiz]

class ResponseAnalyticsMyLastRecordQuizzes(BaseModel):
    result: list[AnalyticsMyLastRecordQuizzes]
    detail: str


