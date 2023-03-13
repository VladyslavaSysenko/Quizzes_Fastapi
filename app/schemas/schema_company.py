from pydantic import BaseModel
from schemas.schema_user import UserList

# create company
class CreateCompany(BaseModel):
    company_name: str
    company_description: str | None = None

# return company
class CompanySchema(CreateCompany):
    company_id: int
    company_owner_id: int

    class Config:
        orm_mode = True

# return list of companies
class CompaniesList(BaseModel):
    companies: list[CompanySchema]

    class Config:
        orm_mode = True
        
# update company
class CompanyUpdate(BaseModel):
    company_name: str | None = None
    company_description: str | None = None

    class Config:
        orm_mode = True

# response user
class ResponseCompanySchema(BaseModel):
    result: CompanySchema

# response users
class ResponseCompaniesList(BaseModel):
    result: CompaniesList