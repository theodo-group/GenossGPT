from ast import List
from fastapi import APIRouter
from genoss.model.llm.local.gpt4all import Gpt4AllLLM
from logger import get_logger

logger = get_logger(__name__)

embeddings_router = APIRouter()


@embeddings_router.post("/embeddings", tags=["Embeddings"])
async def post_embeddings(
    model: str,
    input: str,
):
    gpt = None
    response = None
    if model == "gpt4all":
        gpt = Gpt4AllLLM(name="gpt4all")

    if gpt is None:
        return List([0.0, 0.0, 0.0])
    response = gpt.generate_embedding(input)

    return response
