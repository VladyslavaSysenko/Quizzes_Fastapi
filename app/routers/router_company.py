from fastapi import APIRouter, Depends
from services.service_company import Service_company
from services.service_auth import get_current_user
from schemas.schema_user import UserSchema
from schemas.schema_company import CreateCompany, CompanyUpdate, ResponseCompaniesList, ResponseCompanySchema
from core.connections import get_db
from databases import Database


router =  APIRouter()

# get all companies
@router.get("/companies", response_model=ResponseCompaniesList, status_code=200)
async def get_all_companies(db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseCompaniesList:
    companies = await Service_company(db=db).get_all()
    return ResponseCompaniesList(result=companies, detail="success")

# get company
@router.get("/company/{company_id}", response_model=ResponseCompanySchema, status_code=200)
async def get_company(company_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseCompanySchema:
    company = await Service_company(db=db).get_by_id(company_id=company_id)
    return ResponseCompanySchema(result=company, detail="success")

# create company
@router.post("/company", response_model=ResponseCompanySchema, status_code=201)
async def sign_up_company(payload: CreateCompany, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseCompanySchema:
    company = await Service_company(db=db).create_company(payload=payload, owner_id=user.user_id)
    return ResponseCompanySchema(result=company, detail="success")

# update company
@router.put("/company/{company_id}", response_model=ResponseCompanySchema, status_code=200)
async def update_company(company_id: int, payload: CompanyUpdate, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseCompanySchema:
    company = await Service_company(db=db, user=user, company_id=company_id).update_company(payload=payload)
    return ResponseCompanySchema(result=company, detail="success")

# delete company
@router.delete("/company/{company_id}", response_model=ResponseCompanySchema, status_code=200)
async def delete_company(company_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseCompanySchema:
    await Service_company(db=db, user=user, company_id=company_id).delete_company()
    return ResponseCompanySchema(detail="success")

# leave company
@router.delete("/company/{company_id}/leave", response_model=ResponseCompanySchema, status_code=200)
async def get_members(company_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseCompanySchema:
    await Service_company(db=db, user=user, company_id=company_id).leave_company()
    return ResponseCompanySchema(detail="success")