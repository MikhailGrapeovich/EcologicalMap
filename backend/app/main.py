import logging.config

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.routers import file
from app.api.main import api_router
from app.config import settings
from app.loggng_config import LOGGING_CONFIG
import uvicorn
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
from uvicorn.config import LOGGING_CONFIG

app = FastAPI(title="exelezator", openapi_url=f"{settings.API_V1_STR}/openapi.json")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любых источников. Можете ограничить список доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки

)
app.include_router(api_router,prefix=settings.API_V1_STR)
app.include_router(file.router, tags=["file"])

if __name__ == "__main__":
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    LOGGING_CONFIG["formatters"]["access"][
        "fmt"] = '%(levelprefix)s %(asctime)s :: %(client_addr)s - "%(request_line)s" %(status_code)s'
    logger.info("START PROJECT")
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8001)