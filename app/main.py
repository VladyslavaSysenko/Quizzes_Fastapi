from fastapi import FastAPI
import uvicorn
from utils import system_config




app = FastAPI()

@app.get("/")
async def root():
    return {
  "status_code": 200,
  "detail": "ok",
  "result": "working"
}

if __name__ == '__main__':
    uvicorn.run('main:app', host=system_config.app_host, port=system_config.app_port, reload=True)