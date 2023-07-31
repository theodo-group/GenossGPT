from fastapi import APIRouter, Body, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel

from genoss.auth.auth_handler import AuthHandler
from genoss.entities.chat.chat_completion import ChatCompletion
from genoss.entities.chat.message import Message
from genoss.services.model_factory import ModelFactory
from logger import get_logger

logger = get_logger(__name__)

completions_router = APIRouter()


class RequestBody(BaseModel):
    model: str
    messages: list[Message]
    temperature: float | None


@completions_router.post("/chat/completions", tags=["Chat Completions"])
async def post_chat_completions(
    # TODO: check if this is the correct way to use Body & Depends
    body: RequestBody = Body(...),  # noqa: B008
    api_key: str = Depends(  # type: ignore[assignment] # noqa: B008
        AuthHandler.check_auth_header, use_cache=False
    ),
) -> ChatCompletion:
    model = ModelFactory.get_model_from_name(body.model, api_key)  # pyright: ignore

    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")

    logger.info(
        f"Received chat completions request for {model.name} with messages {body.messages[-1].content}"
    )

    # TODO: Add temperature to request body
    return model.generate_answer(body.messages)
