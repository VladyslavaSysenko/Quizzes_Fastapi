from fastapi import APIRouter, Depends
from services.service_quiz import Service_quiz
from services.service_auth import get_current_user
from schemas.schema_user import UserSchema
from schemas.schema_quiz import ResponseQuizSchema, ResponseQuizzesList, QuizCreate, QuizUpdate
from core.connections import get_db
from databases import Database


router =  APIRouter()


# get quiz
@router.get("/company/{company_id}/quiz/{quiz_id}", response_model=ResponseQuizSchema, status_code=200)
async def get_quiz(quiz_id: int, company_id:int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseQuizSchema:
    quiz = await Service_quiz(db=db, company_id=company_id).get_quiz_by_id(quiz_id=quiz_id)
    return ResponseQuizSchema(result=quiz, detail="success")

# get all quizzes
@router.get("/company/{company_id}/quizzes", response_model=ResponseQuizzesList, status_code=200)
async def get_quizzes(company_id:int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseQuizzesList:
    quizzes = await Service_quiz(db=db, company_id=company_id, user=user).get_all_quizzes()
    return ResponseQuizzesList(result=quizzes, detail="success")

# create quiz
@router.post("/company/{company_id}/quiz", response_model=ResponseQuizSchema, status_code=200)
async def sign_up_quiz(company_id:int, payload: QuizCreate, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseQuizSchema:
    quiz = await Service_quiz(db=db, company_id=company_id, user=user).create_quiz(payload=payload)
    return ResponseQuizSchema(result=quiz, detail="success")

# update quiz
@router.put("/company/{company_id}/quiz/{quiz_id}", response_model=ResponseQuizSchema, status_code=200)
async def update_quiz(quiz_id: int, company_id:int, payload: QuizUpdate, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseQuizSchema:
    quiz = await Service_quiz(db=db, user=user, company_id=company_id).update_quiz(payload=payload, quiz_id=quiz_id)
    return ResponseQuizSchema(result=quiz, detail="success")

# delete quiz 
@router.delete("/company/{company_id}/quiz/{quiz_id}", response_model=ResponseQuizSchema, status_code=200)
async def delete_quiz(quiz_id: int, company_id:int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseQuizSchema:
    await Service_quiz(db=db, user=user, company_id=company_id).delete_quiz(quiz_id=quiz_id)
    return ResponseQuizSchema(detail="success")