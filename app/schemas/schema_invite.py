from pydantic import BaseModel, validator
from fastapi import HTTPException, status

# create invite
class CreateInvite(BaseModel):
    invite_from_company_id: int
    invite_to_user_id: int
    invite_message: str

    @validator('invite_message')
    def check_str_not_empty(cls, v):
        if isinstance(v, str):
            if len(v) < 1:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Message cannot be empty")
        return v
    
    class Config:
        orm_mode = True

# return invite
class InviteSchema(CreateInvite):
    invite_id: int


# return list of invites
class InvitesList(BaseModel):
    invites: list[InviteSchema]

    class Config:
        orm_mode = True
        
# response invite
class ResponseInviteSchema(BaseModel):
    result: InviteSchema | None
    detail: str

# response invites
class ResponseInvitesList(BaseModel):
    result: InvitesList
    detail: str