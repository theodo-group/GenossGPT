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
    if model == "gpt4all":
        gpt = Gpt4AllLLM(name="gpt4all")
    else:
        raise NotImplementedError("Model can not be anything else than gpt4all.")

    response = gpt.generate_embedding(input)
    return response
