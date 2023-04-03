from schemas.schema_user import UserSchema
from schemas.schema_notification import NotificationSchema, NotificationsList
from db.models import Notification
from fastapi import status, HTTPException
from sqlalchemy import select, delete, update
from databases import Database

class Service_notification:
    def __init__(self, db: Database, user: UserSchema, notification_id: int = None) -> None:
        self.db = db
        self.user = user
        self.notification_id = notification_id


    async def get_all_notifications(self) -> NotificationsList:
        query = select(Notification).where(Notification.notification_user_id == self.user.user_id)
        notifications = await self.db.fetch_all(query)
        return NotificationsList(notifications=notifications)


    async def get_notification_by_id(self, notification_id:str) -> NotificationSchema:
        query = select(Notification).where(Notification.notification_id == notification_id)
        notification = await self.db.fetch_one(query)
        if not notification:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        if notification.notification_user_id != self.user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your notification")
        return NotificationSchema(**notification)
    

    async def change_notification_status(self) -> NotificationSchema:
        # check if user's notification
        notification = await self.get_notification_by_id(notification_id=self.notification_id)
        # change status
        query = update(Notification).where(Notification.notification_id == self.notification_id).values(
                notification_status = True if notification.notification_status == False else False
        ).returning(Notification)
        notification = await self.db.fetch_one(query)
        return NotificationSchema(**notification)


    async def delete_notification(self, notification_id:int) -> status:
        # check if user's notification
        await self.get_notification_by_id(notification_id=notification_id)
        # delete notification
        query = delete(Notification).where(Notification.notification_id == notification_id)
        await self.db.execute(query)
        return status.HTTP_200_OK