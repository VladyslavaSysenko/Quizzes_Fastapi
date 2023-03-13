from schemas.schema_company import CompaniesList, CompanySchema, CreateCompany, CompanyUpdate, ResponseCompaniesList, ResponseCompanySchema
from db.models import Company
from utils.password_hasher import Hasher
from fastapi import HTTPException, status
from sqlalchemy import select, insert, delete, update
from databases import Database

class Service_company:
    
    def __init__(self, db: Database) -> None:
        self.db = db

    async def get_all(self) -> CompaniesList:
        query = select(Company)
        companies = await self.db.fetch_all(query)
        return CompaniesList(companies=companies)

    async def get_by_id(self, company_id: int) -> CompanySchema:
        query = select(Company).where(Company.company_id == company_id)
        company = await self.db.fetch_one(query)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        return CompanySchema(**company)

    async def create(self, payload:CreateCompany, owner_id: int) -> CompanySchema:
        query = insert(Company).values(
            company_name = payload.company_name,
            company_owner_id = owner_id,
            company_description = payload.company_description
        ).returning(Company)
        company = await self.db.fetch_one(query)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        return CompanySchema(**company)

    async def delete_company(self, company_id: int) -> status:
        query = delete(Company).where(Company.company_id == company_id)
        await self.db.execute(query)
        # check if deleted
        query = select(Company).where(Company.company_id == company_id)
        company = await self.db.fetch_one(query)
        if company:
            raise HTTPException(status_code=500, detail="Something went wrong")
        return status.HTTP_200_OK

    async def update_company(self, company_id: int, payload:CompanyUpdate) -> CompanySchema:
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
            raise HTTPException(status_code=400, detail="Nothing to change")
        return changed_values