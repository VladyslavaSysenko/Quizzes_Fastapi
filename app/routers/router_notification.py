from fastapi import APIRouter, Depends
from services.service_notification import Service_notification
from services.service_auth import get_current_user
from schemas.schema_user import UserSchema
from schemas.schema_notification import ResponseNotificationSchema, ResponseNotificationsList
from core.connections import get_db
from databases import Database


router =  APIRouter()

# get all notifications
@router.get("/notifications", response_model=ResponseNotificationsList, status_code=200)
async def get_notifications(db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseNotificationsList:
    notifications = await Service_notification(db=db, user=user).get_all_notifications()
    return ResponseNotificationsList(result=notifications, detail="success")

# get notification
@router.get("/notification/{notification_id}", response_model=ResponseNotificationSchema, status_code=200)
async def get_notification(notification_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseNotificationSchema:
    notification = await Service_notification(db=db, user=user, notification_id=notification_id).get_notification_by_id(notification_id=notification_id)
    return ResponseNotificationSchema(result=notification, detail="success")

# change status
@router.post("/notification/{notification_id}/status", response_model=ResponseNotificationSchema, status_code=200)
async def change_notification_status(notification_id:int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseNotificationSchema:
    notifications = await Service_notification(db=db, user=user, notification_id=notification_id).change_notification_status()
    return ResponseNotificationSchema(result=notifications, detail="success")

# delete notification 
@router.delete("/notification/{notification_id}", response_model=ResponseNotificationSchema, status_code=200)
async def delete_notification(notification_id: int, db: Database = Depends(get_db), user: UserSchema = Depends(get_current_user)) -> ResponseNotificationSchema:
    await Service_notification(db=db, user=user).delete_notification(notification_id=notification_id)
    return ResponseNotificationSchema(detail="success")