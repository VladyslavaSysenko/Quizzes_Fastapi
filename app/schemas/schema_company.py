from pydantic import BaseModel, validator
from fastapi import HTTPException, status

# create company
class CreateCompany(BaseModel):
    company_name: str
    company_description: str | None = None

    @validator('company_name')
    def check_str_not_empty(cls, v):
        if isinstance(v, str):
            if len(v) < 1:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Name cannot be empty")
        return v

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

    @validator('company_name')
    def check_str_not_empty(cls, v):
        if isinstance(v, str):
            if len(v) < 1:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Name cannot be empty")
        return v

    class Config:
        orm_mode = True

# response company
class ResponseCompanySchema(BaseModel):
    result: CompanySchema | None
    detail: str

# response companies
class ResponseCompaniesList(BaseModel):
    result: CompaniesList | None
    detail: str