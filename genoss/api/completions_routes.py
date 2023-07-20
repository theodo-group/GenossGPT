from fastapi import APIRouter, Body, HTTPException

from genoss.chat.messages import Message
from genoss.services.model_factory import ModelFactory
from logger import get_logger
from typing import List, Dict, Optional
from pydantic import BaseModel

logger = get_logger(__name__)

completions_router = APIRouter()


class RequestBody(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float]


@completions_router.post("/chat/completions", tags=["Chat Completions"])
async def post_chat_completions(body: RequestBody = Body(...)) -> Dict:
    model = ModelFactory.get_model_from_name(body.model)

    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")

    logger.info(
        f"Received chat completions request for {model.name} with messages {body.messages[-1].content}"
    )

    return model.generate_answer(body.messages[-1].content)
