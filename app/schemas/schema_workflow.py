from pydantic import BaseModel
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


# response quiz
class ResponseWorkflowSchema(BaseModel):
    result: WorkflowSchema | None
    detail: str | None