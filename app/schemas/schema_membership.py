from pydantic import BaseModel
from typing import Literal

# create membership
class CreateMembership(BaseModel):
    membership_user_id: int
    membership_company_id: int
    membership_role: Literal["owner", "admin", "user"]

    class Config:
        orm_mode = True


# membership
class MembershipSchema(CreateMembership):
    membership_id: int


# list of memberships
class MembershipsList(BaseModel):
    users: list[MembershipSchema]

    class Config:
        orm_mode = True


# add admin
class AddAdmin(BaseModel):
    user_id: int

# response membership
class ResponseMembershipSchema(BaseModel):
    result: MembershipSchema | None
    detail: str

# response memberships
class ResponseMembershipsList(BaseModel):
    result: MembershipsList | None
    detail: str