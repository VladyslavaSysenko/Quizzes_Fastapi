from schemas.schema_company import CompaniesList, CompanySchema, CreateCompany, CompanyUpdate
from schemas.schema_user import UserSchema
from db.models import Company
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
        return CompanySchema(**company)


    async def delete_company(self, company_id: int) -> status:
        # check if company exists
        company = await self.get_by_id(company_id=company_id)

        # check if user tries to delete his company
        self.check_id(company=company)

        # delete company
        query = delete(Company).where(Company.company_id == company_id)
        await self.db.execute(query)
        return status.HTTP_200_OK


    async def update_company(self, company_id: int, payload:CompanyUpdate) -> CompanySchema:
        # check if company exists
        company = await self.get_by_id(company_id=company_id)

        # check if user tries to update his company
        self.check_id(company=company)

        # update company
        changed_values = self.get_changed_values(payload=payload)
        query = update(Company).where(Company.company_id == company_id).values(
            changed_values
        ).returning(Company)
        company = await self.db.fetch_one(query)
        return CompanySchema(**company)
            

    def get_changed_values(self, payload:CompanyUpdate) -> dict:
        changed_values = {x[0]:x[1] for x in payload if x[1]}
        # if nothing changed
        if changed_values == {}:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nothing to change")
        return changed_values
    

    def check_id(self, company: CompanySchema) -> status:
        if self.user.user_id != company.company_owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your company")
        return status.HTTP_200_OK