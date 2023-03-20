from schemas.schema_user import UserSchema
from schemas.schema_membership import MembershipsList
from db.models import Membership
from fastapi import status
from sqlalchemy import select, insert, delete
from databases import Database

class Service_membership:
    def __init__(self, db: Database, user: UserSchema = None, company_id: int = None) -> None:
        self.db = db
        self.user = user
        self.company_id = company_id


    async def get_members(self) -> MembershipsList:
        query = select(Membership).where(Membership.membership_company_id == self.company_id)
        members = await self.db.fetch_all(query)
        return MembershipsList(users=members)


    async def delete_membership(self, member_id: int) -> status:
        #delete member
        query = delete(Membership).where(
            Membership.membership_company_id == self.company_id,
            Membership.membership_user_id == member_id
            )
        await self.db.execute(query)
        return status.HTTP_200_OK


    async def create_membership(self, member_id:int) -> status:
        query=insert(Membership).values(
            membership_user_id = member_id,
            membership_company_id = self.company_id
        )
        await self.db.execute(query)
        return status.HTTP_201_CREATED