from pydantic import BaseModel

# create invite
class CreateInvite(BaseModel):
    invite_from_company_id: int
    invite_to_user_id: int
    invite_message: str
    
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
    detail: str | None

# response invites
class ResponseInvitesList(BaseModel):
    result: InvitesList