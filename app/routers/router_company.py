from fastapi import APIRouter, Depends
from services.service_company import Service_company
from services.service_auth import get_current_user
from schemas.schema_user import UserSchema
from schemas.schema_company import CreateCompany, CompanyUpdate, ResponseCompaniesList, ResponseCompanySchema
from schemas.schema_membership import ResponseMembershipsList, AddAdmin, ResponseMembershipSchema
from core.connections import get_db
from databases import Database


router =  APIRouter()

# get all companies
@router.get("/companies", response_model=ResponseCompaniesList, status_code=200)
async def get_all_companies(db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseCompaniesList:
    companies = await Service_company(db=db).get_all()
    return ResponseCompaniesList(result=companies)

# get company
@router.get("/company/{company_id}", response_model=ResponseCompanySchema, status_code=200)
async def get_company(company_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseCompanySchema:
    company = await Service_company(db=db).get_by_id(company_id=company_id)
    return ResponseCompanySchema(result=company)

# create company
@router.post("/company", response_model=ResponseCompanySchema, status_code=201)
async def sign_up_company(payload: CreateCompany, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseCompanySchema:
    company = await Service_company(db=db).create_company(payload=payload, owner_id=user.user_id)
    return ResponseCompanySchema(result=company)

# update company
@router.put("/company/{company_id}", response_model=ResponseCompanySchema, status_code=200)
async def update_company(company_id: int, payload: CompanyUpdate, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseCompanySchema:
    company = await Service_company(db=db, user=user, company_id=company_id).update_company(payload=payload)
    return ResponseCompanySchema(result=company)

# delete company
@router.delete("/company/{company_id}", response_model=ResponseCompanySchema, status_code=200)
async def delete_company(company_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseCompanySchema:
    await Service_company(db=db, user=user, company_id=company_id).delete_company()
    return ResponseCompanySchema(detail="success")

# get all members
@router.get("/company/{company_id}/members", response_model=ResponseMembershipsList, status_code=200)
async def get_members(company_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseMembershipsList:
    users = await Service_company(db=db, company_id=company_id, user=user).get_members()
    return ResponseMembershipsList(result=users)

# delete member
@router.delete("/company/{company_id}/member/{member_id}", response_model=ResponseMembershipSchema, status_code=200)
async def get_members(company_id: int, member_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseMembershipSchema:
    await Service_company(db=db, user=user, company_id=company_id).delete_member(member_id=member_id)
    return ResponseMembershipSchema(detail="success")

# leave company
@router.delete("/company/{company_id}/leave", response_model=ResponseCompanySchema, status_code=200)
async def get_members(company_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseCompanySchema:
    await Service_company(db=db, user=user, company_id=company_id).leave_company()
    return ResponseCompanySchema(detail="success")

# get all admins
@router.get("/company/{company_id}/admins", response_model=ResponseMembershipsList, status_code=200)
async def get_admins(company_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseMembershipsList:
    admins = await Service_company(db=db, company_id=company_id, user=user).get_members(role="admin")
    return ResponseMembershipsList(result=admins)

# create admin
@router.post("/company/{company_id}/admin", response_model=ResponseMembershipSchema, status_code=200)
async def sign_up_company(company_id: int, payload: AddAdmin, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseMembershipSchema:
    membership = await Service_company(db=db, company_id=company_id, user=user).create_admin(member_id=payload.user_id)
    return ResponseMembershipSchema(result=membership, detail="success")

# downgrade admin
@router.delete("/company/{company_id}/admin/{user_id}", response_model=ResponseMembershipSchema, status_code=200)
async def sign_up_company(company_id: int, user_id:int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseMembershipSchema:
    membership = await Service_company(db=db, company_id=company_id, user=user).downgrade_role(member_id=user_id, new_role="user")
    return ResponseMembershipSchema(result=membership, detail="success")
