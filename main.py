import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from logger import get_logger
from routes.completions_routes import completions_router

logger = get_logger(__name__)


app = FastAPI()

app.include_router(completions_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
