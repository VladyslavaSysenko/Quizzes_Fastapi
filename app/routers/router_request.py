from fastapi import APIRouter, Depends
from services.service_request import Service_request
from services.service_auth import get_current_user
from schemas.schema_user import UserSchema
from schemas.schema_request import ResponseRequestSchema, ResponseRequestsList, CreateRequest
from core.connections import get_db
from databases import Database


router =  APIRouter()

# get company requests
@router.get("/request/company/{company_id}", response_model=ResponseRequestsList, status_code=200)
async def get_company_requests(company_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseRequestsList:
    requests = await Service_request(db=db, company_id=company_id, user=user).get_company_requests()
    return ResponseRequestsList(result=requests, detail="success")

# get company requests
@router.get("/request/my", response_model=ResponseRequestsList, status_code=200)
async def get_my_requests(db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseRequestsList:
    requests = await Service_request(db=db, user=user).get_my()
    return ResponseRequestsList(result=requests, detail="success")

# accept request
@router.get("/request/{request_id}/accept", response_model=ResponseRequestSchema, status_code=200)
async def accept_request(request_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseRequestSchema:
    await Service_request(db=db, user=user).accept_request(request_id=request_id)
    return ResponseRequestSchema(detail="success")

# decline request
@router.get("/request/{request_id}/decline", response_model=ResponseRequestSchema, status_code=200)
async def decline_request(request_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseRequestSchema:
    await Service_request(db=db, user=user).decline_request(request_id=request_id)
    return ResponseRequestSchema(detail="success")

# send request
@router.post("/request", response_model=ResponseRequestSchema, status_code=200)
async def create_request(payload: CreateRequest, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseRequestSchema:
    request = await Service_request(db=db, user=user, company_id=payload.request_to_company_id).create(payload=payload)
    return ResponseRequestSchema(result=request, detail="success")

# cancel my request
@router.delete("/request/{request_id}", response_model=ResponseRequestSchema, status_code=200)
async def delete_request(request_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseRequestSchema:
    await Service_request(db=db, user=user).delete_request(request_id=request_id)
    return ResponseRequestSchema(detail="success")
