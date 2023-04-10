from pydantic import BaseModel, validator
from fastapi import HTTPException, status
from datetime import datetime


# notification schema
class NotificationSchema(BaseModel):
    notification_id: int
    notification_user_id: int
    notification_quiz_id: int
    notification_company_id: int
    notification_text: str
    notification_status: bool
    notification_time: datetime

    @validator('notification_text')
    def check_str_not_empty(cls, v):
        if isinstance(v, str):
            if len(v) < 1:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="String cannot be empty")
        return v

    class Config:
        orm_mode = True


# notifications list
class NotificationsList(BaseModel):
    notifications: list[NotificationSchema]


# response notification
class ResponseNotificationSchema(BaseModel):
    result: NotificationSchema | None
    detail: str


# response notifications list
class ResponseNotificationsList(BaseModel):
    result: NotificationsList
    detail: str