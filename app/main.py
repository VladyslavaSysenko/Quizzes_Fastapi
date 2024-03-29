from fastapi import FastAPI
import uvicorn
from core import connections, system_config
from routers import router_user, router_auth, router_company, router_invite, router_request, router_membership, router_quiz, router_data, router_analytics, router_notification
from core.connections import get_db, get_redis
from utils.apscheduler import start_scheduler
app = FastAPI()


@app.on_event("startup")
async def startup():
    await connections.connect_to_db()
    await connections.connect_to_redis()
    start_scheduler()

@app.on_event("shutdown")
async def shutdown():
    await connections.disconnect_from_db()
    await connections.disconnect_from_redis()

@app.get("/")
async def root():
    return {
  "status_code": 200,
  "detail": "ok",
  "result": "working"
}

app.include_router(router_user.router, prefix="", tags=["users"])
app.include_router(router_auth.router, prefix="/auth", tags=["auth"])
app.include_router(router_company.router, prefix="", tags=["company"])
app.include_router(router_membership.router, prefix='', tags=["membership"])
app.include_router(router_invite.router, prefix="", tags=["invite"])
app.include_router(router_request.router, prefix="", tags=["request"])
app.include_router(router_quiz.router, prefix='', tags=["quiz"])
app.include_router(router_data.router, prefix="", tags=["quiz_data"])
app.include_router(router_analytics.router, prefix="", tags=["analytics"])
app.include_router(router_notification.router, prefix="", tags=["notification"])

if __name__ == '__main__':
    uvicorn.run('main:app', host=system_config.app_host, port=system_config.app_port, reload=True)