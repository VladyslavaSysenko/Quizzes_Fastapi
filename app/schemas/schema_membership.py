from pydantic import BaseModel

# create membership
class CreateMembership(BaseModel):
    membership_user_id: int
    membership_company_id: int

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


# response membership
class ResponseMembershipSchema(BaseModel):
    result: MembershipSchema | None
    detail: str | None


# response memberships
class ResponseMembershipsList(BaseModel):
    result: MembershipsList | None
    detail: str | None