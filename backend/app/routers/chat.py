from fastapi import APIRouter
from pydantic import BaseModel

from app.prompts import REFLECTIVE_SYSTEM_PROMPT
from app.services.llm import get_completion


router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Uses the real reflective system prompt as of today. Still no
    mode switching (Day 6), no persistence (Day 6/later), and no
    crisis check yet (Days 9-10) — one thing added per day, on purpose.
    """
    reply = get_completion(
        request.message,
        system_prompt=REFLECTIVE_SYSTEM_PROMPT
    )
    return ChatResponse(response=reply)