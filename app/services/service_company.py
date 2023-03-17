from schemas.schema_company import CompaniesList, CompanySchema, CreateCompany, CompanyUpdate
from schemas.schema_user import UserSchema
from schemas.schema_membership import MembershipsList
from db.models import Company, Membership
from fastapi import HTTPException, status
from sqlalchemy import select, insert, delete, update
from databases import Database

class Service_company:
    
    def __init__(self, db: Database, user: UserSchema = None) -> None:
        self.db = db
        self.user = user


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


    async def create(self, payload:CreateCompany, owner_id: int) -> CompanySchema:
        # error if no name
        if payload.company_name == "":
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No name provided")
        # create company
        query = insert(Company).values(
            company_name = payload.company_name,
            company_owner_id = owner_id,
            company_description = payload.company_description
        ).returning(Company)
        company = await self.db.fetch_one(query)
        # add owner to members of the company
        query=insert(Membership).values(
            membership_user_id = owner_id,
            membership_company_id = company.company_owner_id
        ).returning(Membership)
        await self.db.execute(query)
        return CompanySchema(**company)


    async def delete_company(self, company_id: int) -> status:
        # check if user tries to delete his company
        await self.check_id(company_id=company_id)

        # delete company
        query = delete(Company).where(Company.company_id == company_id)
        await self.db.execute(query)
        return status.HTTP_200_OK


    async def update_company(self, company_id: int, payload:CompanyUpdate) -> CompanySchema:
        # check if user tries to update his company
        await self.check_id(company_id=company_id)

        # update company
        changed_values = self.get_changed_values(payload=payload)
        query = update(Company).where(Company.company_id == company_id).values(
            changed_values
        ).returning(Company)
        company = await self.db.fetch_one(query)
        return CompanySchema(**company)
            

    async def get_members(self, company_id: int) -> MembershipsList:
        query = select(Membership).where(Membership.membership_company_id == company_id)
        members = await self.db.fetch_all(query)
        return MembershipsList(users=members)


    async def delete_member(self, company_id: int, member_id: int) -> status:
        # check if user's company
        await self.check_id(company_id=company_id)

        #delete member
        query = delete(Membership).where(
            Membership.membership_company_id == company_id,
            Membership.membership_user_id == member_id
            )
        await self.db.execute(query)
        return status.HTTP_200_OK


    async def leave_company(self, company_id: int) -> status:
        # check if user is member
        await self.is_member(company_id=company_id)
        # leave company
        query = delete(Membership).where(
            Membership.membership_company_id == company_id,
            Membership.membership_user_id == self.user.user_id
            )
        await self.db.execute(query)
        return status.HTTP_200_OK

    def get_changed_values(self, payload:CompanyUpdate) -> dict:
        changed_values = {x[0]:x[1] for x in payload if x[1]}
        # if nothing changed
        if changed_values == {}:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nothing to change")
        return changed_values
    

    async def check_id(self, company_id: str) -> status:
        company = await self.get_by_id(company_id=company_id)
        if self.user.user_id != company.company_owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your company")
        return status.HTTP_200_OK
    
    async def is_member(self, company_id: int) -> status:
        company_members = await self.get_members(company_id=company_id)
        if self.user.user_id not in [member.membership_user_id for member in company_members.users]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not a member of this company")
        return status.HTTP_200_OK