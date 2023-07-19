from fastapi import APIRouter, Body, HTTPException
from genoss.model.gpt4all import gpt_4_all
from logger import get_logger
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

logger = get_logger(__name__)

completions_router = APIRouter()


class Message(BaseModel):
    role: str
    content: str


class RequestBody(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float]


@completions_router.post("/chat/completions", tags=["Chat Completions"])
async def post_chat_completions(body: RequestBody = Body(...)) -> Dict:
    model = body.model
    if model == "gpt4all":
        gpt = gpt_4_all(name="gpt4all")
        response = gpt.generate_answer(body.messages[-1].content)
        logger.info(
            f"Received chat completions request for {body.model} with messages {body.messages[-1].content}"
        )

        return response

    else:
        raise HTTPException(status_code=404, detail="Model not found")