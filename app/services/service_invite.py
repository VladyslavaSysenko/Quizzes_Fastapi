from schemas.schema_invite import InvitesList, InviteSchema, CreateInvite
from schemas.schema_user import UserSchema
from services.service_company import Service_company
from services.service_user import Service_user
from services.service_membership import Service_membership
from db.models import Invite
from fastapi import HTTPException, status
from sqlalchemy import select, insert, delete
from databases import Database

class Service_invite:
    
    def __init__(self, db: Database, user: UserSchema = None, company_id: int = None) -> None:
        self.db = db
        self.company_id = company_id
        self.user = user
    

    async def get_company_invites(self) -> InvitesList:
        await Service_company(db=self.db, user=self.user, company_id=self.company_id).check_id()
        query = select(Invite).where(Invite.invite_from_company_id == self.company_id)
        invites = await self.db.fetch_all(query)
        return InvitesList(invites=invites)
    

    async def get_my(self) -> InvitesList:
        query = select(Invite).where(Invite.invite_to_user_id == self.user.user_id)
        invites = await self.db.fetch_all(query)
        return InvitesList(invites=invites)


    async def get_by_id(self, invite_id: int) -> InviteSchema:
        query = select(Invite).where(Invite.invite_id == invite_id)
        invite = await self.db.fetch_one(query)
        if not invite:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite not found")
        return InviteSchema(**invite)


    async def create(self, payload:CreateInvite) -> InviteSchema:
        # error if no name
        if payload.invite_message == "":
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No message provided")
        # check if user is admin or owner and if to user exists
        await Service_user(db=self.db, user=self.user).get_by_id(user_id=payload.invite_to_user_id)
        await Service_company(db=self.db, user=self.user, company_id=payload.invite_from_company_id).check_id()
        # check if user is not a member
        await self.is_member(user_id=payload.invite_to_user_id)
        # check if invite already exists
        await self.invite_exists(user_id=payload.invite_to_user_id)
        # create invite
        query = insert(Invite).values(
            invite_to_user_id = payload.invite_to_user_id,
            invite_message = payload.invite_message,
            invite_from_company_id = self.company_id
        ).returning(Invite)
        invite = await self.db.fetch_one(query)
        return InviteSchema(**invite)


    async def delete_invite(self, invite_id: int) -> status:
        invite = await self.get_by_id(invite_id=invite_id)
        # check if user is admin or owner
        await Service_company(db=self.db, user=self.user, company_id=invite.invite_from_company_id).check_id()
        # delete invite
        delete(Invite).where(Invite.invite_id == invite_id)
        return status.HTTP_200_OK
    

    async def accept_invite(self, invite_id: int) -> status:
        invite = await self.get_by_id(invite_id=invite_id)
        # check if user's invite
        await self.check_invite_id(invite_id=invite_id)
        # accept invite
        await Service_membership(db=self.db, company_id=invite.invite_from_company_id).create_membership(
            member_id=invite.invite_to_user_id, role="user")
        # delete invite
        delete(Invite).where(Invite.invite_id == invite_id)
        return status.HTTP_200_OK


    async def decline_invite(self, invite_id: int) -> status:
        invite = await self.get_by_id(invite_id=invite_id)
        # check if user's invite
        await self.check_invite_id(invite_id=invite_id)
        # decline invite
        delete(Invite).where(Invite.invite_id == invite_id)
        return status.HTTP_200_OK


    async def check_invite_id(self, invite_id: int) -> None:
        users_invites = await self.get_my()
        if invite_id not in [invite.invite_id for invite in users_invites.invites]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It's not your invite")
        
    async def invite_exists(self, user_id: int) -> None:
        company_invites = await self.get_my()
        if user_id in [invite.invite_to_user_id for invite in company_invites.invites]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invite already sent")

    async def is_member(self, user_id: str) -> status:
        company_members = await Service_membership(db=self.db, user=self.user, company_id=self.company_id).get_members()
        if user_id in [member.membership_user_id for member in company_members.users]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already a member of the company")
        return status.HTTP_200_OK