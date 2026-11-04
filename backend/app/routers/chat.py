from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from app.prompts import COMFORT_SYSTEM_PROMPT, REFLECTIVE_SYSTEM_PROMPT
from app.services.llm import get_completion

router = APIRouter(prefix="/chat", tags=["chat"])

MODE_PROMPTS = {
    "reflective": REFLECTIVE_SYSTEM_PROMPT,
    "comfort": COMFORT_SYSTEM_PROMPT,
}


class ChatRequest(BaseModel):
    message: str
    mode: Literal["reflective", "comfort"] = "reflective"


class ChatResponse(BaseModel):
    response: str
    mode: str


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    system_prompt = MODE_PROMPTS[request.mode]
    reply = get_completion(request.message, system_prompt=system_prompt)
    return ChatResponse(response=reply, mode=request.mode)