from fastapi import APIRouter, Depends, HTTPException, status
from services.service_company import Service_company
from services.service_auth import get_current_user
from schemas.schema_user import UserList
from schemas.schema_company import CompaniesList, CompanySchema, CreateCompany, CompanyUpdate, ResponseCompaniesList, ResponseCompanySchema
from core.connections import get_db
from databases import Database


router =  APIRouter()

# get all companies
@router.get("/companies", response_model=ResponseCompaniesList, status_code=200)
async def get_all_companies(db: Database = Depends(get_db), user: UserList = Depends(get_current_user)) -> ResponseCompaniesList:
    companies = await Service_company(db=db).get_all()
    return ResponseCompaniesList(result=companies)

# get company
@router.get("/company/{company_id}", response_model=ResponseCompanySchema, status_code=200)
async def get_company(company_id: int, db: Database = Depends(get_db), user: UserList = Depends(get_current_user)) -> ResponseCompanySchema:
    company = await Service_company(db=db).get_by_id(company_id=company_id)
    return ResponseCompanySchema(result=company)

# create company
@router.post("/company", response_model=ResponseCompanySchema, status_code=201)
async def sign_up_company(payload: CreateCompany, db: Database = Depends(get_db), user: UserList = Depends(get_current_user)) -> ResponseCompanySchema:
    # error if no name
    if payload.company_name == "":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No name provided")
    company = await Service_company(db=db).create(payload=payload, owner_id=user.user_id)
    return ResponseCompanySchema(result=company)

# update company
@router.put("/company/{company_id}", response_model=ResponseCompanySchema, status_code=200)
async def update_company(company_id: int, payload: CompanyUpdate, db: Database = Depends(get_db), user: UserList = Depends(get_current_user)) -> ResponseCompanySchema:
    # check if company exists
    company = await Service_company(db=db).get_by_id(company_id=company_id)
   
    # check if user tries to update his company
    Service_company(db=db).check_id(user=user, company=company)
    
    # update company
    company = await Service_company(db=db).update_company(company_id=company_id, payload=payload)
    return ResponseCompanySchema(result=company)

# delete company
@router.delete("/company/{company_id}", status_code=200)
async def delete_company(company_id: int, db: Database = Depends(get_db), user: UserList = Depends(get_current_user)) -> None:
    # check if company exists
    company = await Service_company(db=db).get_by_id(company_id=company_id)

    # check if user tries to delete his company
    Service_company(db=db).check_id(user=user, company=company)
    
    # delete company
    await Service_company(db=db).delete_company(company_id=company_id)
