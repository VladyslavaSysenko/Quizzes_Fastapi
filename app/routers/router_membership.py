from fastapi import APIRouter, Depends
from services.service_company import Service_company
from services.service_auth import get_current_user
from schemas.schema_user import UserSchema
from schemas.schema_membership import ResponseMembershipsList, AddMembership, ResponseMembershipSchema
from core.connections import get_db
from databases import Database


router =  APIRouter()

# get all members
@router.get("/company/{company_id}/members", response_model=ResponseMembershipsList, status_code=200)
async def get_members(company_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseMembershipsList:
    users = await Service_company(db=db, company_id=company_id, user=user).get_members()
    return ResponseMembershipsList(result=users, detail="success")

# delete member
@router.delete("/company/{company_id}/member/{member_id}", response_model=ResponseMembershipSchema, status_code=200)
async def get_members(company_id: int, member_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseMembershipSchema:
    await Service_company(db=db, user=user, company_id=company_id).delete_member(member_id=member_id)
    return ResponseMembershipSchema(detail="success")

# get all admins
@router.get("/company/{company_id}/admins", response_model=ResponseMembershipsList, status_code=200)
async def get_admins(company_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseMembershipsList:
    admins = await Service_company(db=db, company_id=company_id, user=user).get_members(role="admin")
    return ResponseMembershipsList(result=admins, detail="success")

# create admin
@router.post("/company/{company_id}/admin", response_model=ResponseMembershipSchema, status_code=200)
async def sign_up_company(company_id: int, payload: AddMembership, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseMembershipSchema:
    membership = await Service_company(db=db, company_id=company_id, user=user).create_admin(member_id=payload.user_id)
    return ResponseMembershipSchema(result=membership, detail="success")

# downgrade admin
@router.delete("/company/{company_id}/admin/{user_id}", response_model=ResponseMembershipSchema, status_code=200)
async def sign_up_company(company_id: int, user_id:int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseMembershipSchema:
    membership = await Service_company(db=db, company_id=company_id, user=user).downgrade_role(member_id=user_id, new_role="user")
    return ResponseMembershipSchema(result=membership, detail="success")

# give ownership of the company to admin and become admin
@router.post("/company/{company_id}/ownership", response_model=ResponseMembershipsList, status_code=200)
async def give_ownership(company_id: int, payload: AddMembership, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseMembershipsList:
    membership = await Service_company(db=db, company_id=company_id, user=user).give_ownership(member_id=payload.user_id)
    return ResponseMembershipsList(result=membership, detail="success")