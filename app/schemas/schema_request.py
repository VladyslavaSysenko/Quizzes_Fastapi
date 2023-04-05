from pydantic import BaseModel

# create request
class CreateRequest(BaseModel):
    request_to_company_id: int
    request_message: str
    
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