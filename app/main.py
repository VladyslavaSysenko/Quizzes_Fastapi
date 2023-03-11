from fastapi import FastAPI, Depends
import uvicorn
from core import connections, system_config
from routers import router_user, router_auth
from core.connections import get_db
from fastapi import Depends
app = FastAPI()


@app.on_event("startup")
async def startup():
    await connections.connect_to_db()
    await connections.connect_to_redis()


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

if __name__ == '__main__':
    uvicorn.run('main:app', host=system_config.app_host, port=system_config.app_port, reload=True)

