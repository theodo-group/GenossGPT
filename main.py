from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from scipy import misc
from logger import get_logger
from genoss.api.completions_routes import completions_router
from genoss.api.embeddings_routes import embeddings_router
from genoss.api.misc_routes import misc_router

import logging
from fastapi.exceptions import RequestValidationError

logger = get_logger(__name__)


app = FastAPI()

app.include_router(completions_router)
app.include_router(embeddings_router)
app.include_router(misc_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    logger.error(f"Received request: {request}")
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
