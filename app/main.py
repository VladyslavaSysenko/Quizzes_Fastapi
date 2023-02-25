from fastapi import FastAPI
import uvicorn
import connections
import system_config

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

if __name__ == '__main__':
    uvicorn.run('main:app', host=system_config.app_host, port=system_config.app_port, reload=True)