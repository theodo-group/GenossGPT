from fastapi import APIRouter
from llm.gpt4all import gpt_4_all
from logger import get_logger
from classes.messages import Messages

logger = get_logger(__name__)

completions_router = APIRouter()


@completions_router.post("/chat/completions", tags=["Chat Completions"])
async def post_chat_completions(
    question: str,
    model: str = "gpt4all",  # make union of all models
) -> str:
    gpt = None
    response = None
    if model == "gpt4all":
        gpt = gpt_4_all(name="gpt4all")

    if gpt is None:
        return "Model not found"
    response = gpt.generate_answer(question)
    logger.info(
        f"Received chat completions request for {model} with messages {question}"
    )
    return response
