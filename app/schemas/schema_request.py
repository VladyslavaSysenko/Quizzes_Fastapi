from pydantic import BaseModel, validator
from fastapi import HTTPException, status

# create request
class CreateRequest(BaseModel):
    request_to_company_id: int
    request_message: str

    @validator('request_message')
    def check_str_not_empty(cls, v):
        if isinstance(v, str):
            if len(v) < 1:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Message cannot be empty")
        return v
    
    class Config:
        orm_mode = True

# return request
class RequestSchema(CreateRequest):
    request_from_user_id: int
    request_id: int


# return list of requests
class RequestsList(BaseModel):
    requests: list[RequestSchema]

    class Config:
        orm_mode = True
        
# response request
class ResponseRequestSchema(BaseModel):
    result: RequestSchema | None
    detail: str

# response requests
class ResponseRequestsList(BaseModel):
    result: RequestsList | None
    detail: str