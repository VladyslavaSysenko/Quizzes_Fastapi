from schemas.schema_company import CompaniesList, CompanySchema, CreateCompany, CompanyUpdate
from schemas.schema_user import UserSchema
from schemas.schema_membership import MembershipsList, MembershipSchema
from services.service_membership import Service_membership
from services.service_user import Service_user
from db.models import Company
from fastapi import HTTPException, status
from sqlalchemy import select, insert, delete, update
from databases import Database

class Service_company:
    
    def __init__(self, db: Database, user: UserSchema = None, company_id:int = None) -> None:
        self.db = db
        self.user = user
        self.company_id = company_id


    async def get_all(self) -> CompaniesList:
        query = select(Company)
        companies = await self.db.fetch_all(query)
        return CompaniesList(companies=companies)


    async def get_by_id(self, company_id: int) -> CompanySchema:
        query = select(Company).where(Company.company_id == company_id)
        company = await self.db.fetch_one(query)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        return CompanySchema(**company)


    async def create_company(self, payload:CreateCompany, owner_id: int) -> CompanySchema:
        # create company
        query = insert(Company).values(
            company_name = payload.company_name,
            company_owner_id = owner_id,
            company_description = payload.company_description
        ).returning(Company)
        company = await self.db.fetch_one(query)
        # add owner to members of the company
        await Service_membership(db=self.db, company_id=company.company_id).create_membership(member_id=owner_id, role="owner")
        return CompanySchema(**company)


    async def delete_company(self) -> status:
        # check if user tries to delete his company
        await self.is_owner()
        # delete company
        query = delete(Company).where(Company.company_id == self.company_id)
        await self.db.execute(query)
        return status.HTTP_200_OK


    async def update_company(self, payload:CompanyUpdate) -> CompanySchema:
        # check if user is admin
        await self.is_owner()
        # update company
        changed_values = self.get_changed_values(payload=payload)
        query = update(Company).where(Company.company_id == self.company_id).values(
            changed_values
        ).returning(Company)
        company = await self.db.fetch_one(query)
        return CompanySchema(**company)
            

    async def delete_member(self, member_id: int) -> status:
        # check if user is owner
        await self.is_owner()
        # check if user doesn't try to delete himself
        if self.user.user_id == member_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot delete yourself")
        #delete member
        await Service_membership(db=self.db, company_id=self.company_id).delete_membership(member_id=member_id)
        return status.HTTP_200_OK


    async def get_members(self, role: str = None) -> MembershipsList:
        # check if company exists
        await self.get_by_id(company_id=self.company_id)
        # get members
        members = await Service_membership(db=self.db, company_id=self.company_id).get_members(role=role)
        return members


    async def leave_company(self) -> status:
        # check if user is member
        if not await self.is_member(member_id=self.user.user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a member of this company")
        # check if user is owner
        if await Service_membership(db=self.db, company_id=self.company_id).get_members(member_id=self.user.user_id, role="owner"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You must give ownership of the company to admin before leaving")
        # leave company
        await Service_membership(db=self.db, company_id=self.company_id).delete_membership(member_id=self.user.user_id)
        return status.HTTP_200_OK


    async def create_admin(self, member_id: int) -> MembershipSchema:
        # check if user's company
        await self.is_owner()
        # check if user exists
        await Service_user(db=self.db, user=self.user).get_by_id(user_id=member_id)
        # check if user exists and is member
        if not await self.is_member(member_id=member_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a member of this company")
        # add admin to members of the company
        membership = await Service_membership(db=self.db, company_id=self.company_id).change_membership(member_id=member_id, role="admin")
        return membership
    
    
    async def downgrade_role(self, member_id: int, new_role: str) -> MembershipSchema:
        # check if user's company
        await self.is_owner()
        # check if user exists
        await Service_user(db=self.db, user=self.user).get_by_id(user_id=member_id)
        # check if user exists and is member
        if not await self.is_member(member_id=member_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a member of this company")
        # downgrade member
        membership = await Service_membership(db=self.db, company_id=self.company_id).change_membership(member_id=member_id, role=new_role)
        return membership
    

    async def give_ownership(self, member_id: int) -> MembershipsList:
        # check if user's company
        await self.is_owner()
        # check if user_to_be_owner exists
        await Service_user(db=self.db, user=self.user).get_by_id(user_id=member_id)
        # check if user_to_be_owner is admin
        if not await Service_company(db=self.db, company_id=self.company_id).is_admin_owner(member_id=member_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not admin")
        # downgrade owner
        new_admin = await Service_membership(db=self.db, company_id=self.company_id).change_membership(member_id=self.user.user_id, role="admin")
        # upgrade admin 
        new_owner = await Service_membership(db=self.db, company_id=self.company_id).change_membership(member_id=member_id, role="owner")
        query = update(Company).where(Company.company_id == self.company_id).values(
            company_owner_id = member_id
        ).returning(Company)
        await self.db.execute(query)
        return MembershipsList(users=[new_owner, new_admin])
        

    def get_changed_values(self, payload:CompanyUpdate) -> CompanyUpdate:
        changed_values = {x[0]:x[1] for x in payload if x[1]}
        # if nothing changed
        if changed_values == {}:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Nothing to change")
        return changed_values

    async def is_owner(self) -> status:
        #check if company exists
        await self.get_by_id(company_id=self.company_id)
        # check if user is owner
        member = await Service_membership(db=self.db, company_id=self.company_id).get_members(role="owner", member_id=self.user.user_id)
        if not bool(member):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your company")
        return status.HTTP_200_OK
    
    async def is_admin_owner(self, member_id:int) -> bool:
        # check if company exists
        await self.get_by_id(company_id=self.company_id)
        # check if user is admin or owner
        member = await Service_membership(db=self.db, company_id=self.company_id).get_members(role=["admin","owner"], member_id=member_id)
        return bool(member)
    

    async def is_member(self, member_id:int) -> bool:
        # check if company exists
        await self.get_by_id(company_id=self.company_id)
        # check if member exists
        user = await Service_user(db=self.db, user=self.user).get_by_id(user_id=member_id)
        await Service_user(db=self.db, user=user).get_by_id(user_id=member_id)
        member = await Service_membership(db=self.db, company_id=self.company_id).get_members(member_id=member_id)
        return bool(member)