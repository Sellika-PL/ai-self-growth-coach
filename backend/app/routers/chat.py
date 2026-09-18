from fastapi import APIRouter
from pydantic import BaseModel

from app.services.llm import get_completion

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Bare-bones today: takes a message, returns a Groq completion.
    No conversation persistence, no mode switching, no crisis check yet —
    those land on Days 6, 6, and 9-10 respectively. Today just proves
    the frontend-to-backend-to-LLM wiring actually works.
    """
    reply = get_completion(request.message)
    return ChatResponse(response=reply)
