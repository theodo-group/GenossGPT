from fastapi import APIRouter

from genoss.llm.local.gpt4all import Gpt4AllLLM
from logger import get_logger

logger = get_logger(__name__)

embeddings_router = APIRouter()


@embeddings_router.post("/embeddings", tags=["Embeddings"])
async def post_embeddings(
    model: str,
    input: str,
) -> list[float]:
    gpt = None
    if model == "gpt4all":
        gpt = Gpt4AllLLM(name="gpt4all")

    if gpt is None:
        return [0.0, 0.0, 0.0]
    response = gpt.generate_embedding(input)

    return response
