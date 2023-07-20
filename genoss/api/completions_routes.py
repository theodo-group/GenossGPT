from typing import Dict, List, Optional

from fastapi import APIRouter, Body, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel

from genoss.auth.auth_handler import AuthHandler
from genoss.entities.chat.message import Message
from genoss.services.model_factory import ModelFactory
from logger import get_logger

logger = get_logger(__name__)

completions_router = APIRouter()


class RequestBody(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float]


@completions_router.post("/chat/completions", tags=["Chat Completions"])
async def post_chat_completions(
    body: RequestBody = Body(...), api_key=Depends(AuthHandler.check_auth_header)
) -> Dict:
    model = ModelFactory.get_model_from_name(body.model, api_key)

    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")

    logger.info(
        f"Received chat completions request for {model.name} with messages {body.messages[-1].content}"
    )

    # TODO: Add temperature to request body
    return model.generate_answer(body.messages[-1].content)
