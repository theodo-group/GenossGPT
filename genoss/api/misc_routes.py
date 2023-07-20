from fastapi import APIRouter
from logger import get_logger

logger = get_logger(__name__)

misc_router = APIRouter()


@misc_router.get("/", tags=["Root"])
async def get_root(
):
    return "Genoss API is running!"
