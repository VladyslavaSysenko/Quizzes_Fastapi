from schemas.schema_request import RequestsList, RequestSchema, CreateRequest
from schemas.schema_user import UserSchema
from services.service_company import Service_company
from services.service_membership import Service_membership
from db.models import Request
from fastapi import HTTPException, status
from sqlalchemy import select, insert, delete
from databases import Database

class Service_request:
    
    def __init__(self, db: Database, user: UserSchema = None, company_id: int = None) -> None:
        self.db = db
        self.company_id = company_id
        self.user = user
    

    async def get_company_requests(self) -> RequestsList:
        await Service_company(db=self.db, user=self.user, company_id=self.company_id).check_id()
        query = select(Request).where(Request.request_to_company_id == self.company_id)
        requests = await self.db.fetch_all(query)
        return RequestsList(requests=requests)
    

    async def get_my(self) -> RequestsList:
        query = select(Request).where(Request.request_from_user_id == self.user.user_id)
        requests = await self.db.fetch_all(query)
        return RequestsList(requests=requests)


    async def get_by_id(self, request_id: int) -> RequestSchema:
        query = select(Request).where(Request.request_id == request_id)
        request = await self.db.fetch_one(query)
        if not request:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
        return RequestSchema(**request)


    async def create(self, payload:CreateRequest) -> RequestSchema:
        # error if no name
        if payload.request_message == "":
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No message provided")
        # check if to company exists
        await Service_company(db=self.db, user=self.user).get_by_id(company_id=payload.request_to_company_id)
        # check if user not member
        await self.is_member()
        # check if request already exists
        await self.request_exists()
        # create request
        query = insert(Request).values(
            request_from_user_id = self.user.user_id,
            request_message = payload.request_message,
            request_to_company_id = self.company_id
        ).returning(Request)
        request = await self.db.fetch_one(query)
        return RequestSchema(**request)


    async def delete_request(self, request_id: int) -> status:
        await self.get_by_id(request_id=request_id)
        # check if user's request
        await self.check_request_id(request_id=request_id)
        # delete request
        query=delete(Request).where(Request.request_id == request_id)
        await self.db.execute(query)
        return status.HTTP_200_OK
    

    async def accept_request(self, request_id: int) -> status:
        request = await self.get_by_id(request_id=request_id)
        # check if user is admin or owner
        await Service_company(db=self.db, user=self.user, company_id=request.request_to_company_id).check_id()
        # accept request
        await Service_membership(db=self.db, company_id=request.request_to_company_id).create_membership(
            member_id=request.request_from_user_id, role="user")
        # delete from requests
        query=delete(Request).where(Request.request_id == request_id)
        await self.db.execute(query)
        return status.HTTP_200_OK


    async def decline_request(self, request_id: int) -> status:
        request = await self.get_by_id(request_id=request_id)
        # check if user is admin or owner
        await Service_company(db=self.db, user=self.user, company_id=request.request_to_company_id).check_id()
        # decline request
        query=delete(Request).where(Request.request_id == request_id)
        await self.db.execute(query)
        return status.HTTP_200_OK


    async def is_member(self) -> status:
        company_members = await Service_membership(db=self.db, user=self.user, company_id=self.company_id).get_members()
        if self.user.user_id in [member.membership_user_id for member in company_members.users]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already a member of the company")
        return status.HTTP_200_OK

    async def request_exists(self) -> None:
        user_requests = await self.get_my()
        if self.company_id in [request.request_to_company_id for request in user_requests.requests]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request already sent")
        

    async def check_request_id(self, request_id: int) -> None:
        users_requests = await self.get_my()
        if request_id not in [request.request_id for request in users_requests.requests]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your request")