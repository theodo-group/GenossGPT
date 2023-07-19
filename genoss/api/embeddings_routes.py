from ast import List
from fastapi import APIRouter
from logger import get_logger
from genoss.model.gpt4all import gpt_4_all


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
        gpt = gpt_4_all(name="gpt4all")

    if gpt is None:
        return List([0.0, 0.0, 0.0])
    response = gpt.generate_embedding(input)

    return response
