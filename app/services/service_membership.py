from schemas.schema_user import UserSchema
from schemas.schema_membership import MembershipsList, MembershipSchema
from db.models import Membership
from fastapi import status
from sqlalchemy import select, insert, delete, update
from databases import Database

class Service_membership:
    def __init__(self, db: Database, user: UserSchema = None, company_id: int = None) -> None:
        self.db = db
        self.user = user
        self.company_id = company_id


    async def get_members(self, role: str | list[str] = None, member_id:int = None) -> MembershipsList | None:
        # get one role
        if role:
            role = [role] if isinstance(role, str) else role
            # get one member
            if member_id:
                query = select(Membership).where(Membership.membership_company_id == self.company_id, Membership.membership_user_id == member_id)\
                                          .filter(Membership.membership_role.in_(role)).order_by(Membership.membership_user_id)
            # get all members
            else:
                query = select(Membership).where(Membership.membership_company_id == self.company_id)\
                                          .filter(Membership.membership_role.in_(role)).order_by(Membership.membership_user_id)
        # get all roles       
        else: 
            # get one member
            if member_id:
                query = select(Membership).where(Membership.membership_company_id == self.company_id, Membership.membership_user_id == member_id)\
                                          .order_by(Membership.membership_user_id)
            # get all members
            else:
                query = select(Membership).where(Membership.membership_company_id == self.company_id).order_by(Membership.membership_user_id)
        members = await self.db.fetch_all(query)
        return MembershipsList(users=members) if members else None


    async def delete_membership(self, member_id: int) -> status:
        #delete member
        query = delete(Membership).where(
            Membership.membership_company_id == self.company_id,
            Membership.membership_user_id == member_id
            )
        await self.db.execute(query)
        return status.HTTP_200_OK


    async def create_membership(self, member_id:int, role: str) -> status:
        query=insert(Membership).values(
            membership_user_id = member_id,
            membership_company_id = self.company_id,
            membership_role = role
        )
        await self.db.execute(query)
        return status.HTTP_201_CREATED
    

    async def change_membership(self, member_id:int, role: str) -> MembershipSchema:
        query = update(Membership).where(
            Membership.membership_user_id == member_id, 
            Membership.membership_company_id == self.company_id).values(
                membership_role = role
                ).returning(Membership)
        membership = await self.db.fetch_one(query)
        return MembershipSchema(**membership)
