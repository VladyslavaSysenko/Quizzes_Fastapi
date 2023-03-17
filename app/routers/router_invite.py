from fastapi import APIRouter, Depends
from services.service_invite import Service_invite
from services.service_auth import get_current_user
from schemas.schema_user import UserSchema
from schemas.schema_invite import ResponseInviteSchema, ResponseInvitesList, CreateInvite
from core.connections import get_db
from databases import Database


router =  APIRouter()

# get company invites
@router.get("/invite/company/{company_id}", response_model=ResponseInvitesList, status_code=200)
async def get_company_invites(company_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseInvitesList:
    invites = await Service_invite(db=db, company_id=company_id, user=user).get_company_invites()
    return ResponseInvitesList(result=invites)

# get my invites
@router.get("/invite/my", response_model=ResponseInvitesList, status_code=200)
async def get_my_invites(db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseInvitesList:
    invites = await Service_invite(db=db, user=user).get_my()
    return ResponseInvitesList(result=invites)

# accept invite
@router.get("/invite/{invite_id}/accept", response_model=ResponseInviteSchema, status_code=200)
async def accept_invite(invite_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseInviteSchema:
    await Service_invite(db=db, user=user).accept_invite(invite_id=invite_id)
    return ResponseInviteSchema(detail="success")

# decline invite
@router.get("/invite/{invite_id}/decline", response_model=ResponseInviteSchema, status_code=200)
async def decline_invite(invite_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseInviteSchema:
    await Service_invite(db=db, user=user).decline_invite(invite_id=invite_id)
    return ResponseInviteSchema(detail="success")

# send invite
@router.post("/invite", response_model=ResponseInviteSchema, status_code=200)
async def create_invite(payload: CreateInvite, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseInviteSchema:
    invite = await Service_invite(db=db, user=user, company_id=payload.invite_from_company_id).create(payload=payload)
    return ResponseInviteSchema(result=invite, detail="success")

# cancel company invite
@router.delete("/invite/{invite_id}", status_code=200)
async def delete_invite(invite_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> None:
    await Service_invite(db=db, user=user).delete_invite(invite_id=invite_id)
    return ResponseInviteSchema(detail="success")