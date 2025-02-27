from fastapi import FastAPI
from api.main import api_router
from app.config import settings
import uvicorn


app = FastAPI(title="exelezator", openapi_url=f"{settings.API_V1_STR}/openapi.json")
app.include_router(api_router,prefix=settings.API_V1_STR)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)