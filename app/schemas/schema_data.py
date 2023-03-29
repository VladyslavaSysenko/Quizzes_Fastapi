from pydantic import BaseModel
from schemas.schema_quiz import QuizSubmitRedis


class Data(BaseModel):
    data: list[QuizSubmitRedis]

class ResponseData(BaseModel):
    result: Data
    detail: str