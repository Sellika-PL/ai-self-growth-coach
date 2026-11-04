from groq import Groq

from app.config import GROQ_API_KEY, GROQ_MODEL


client = Groq(api_key=GROQ_API_KEY)


def get_completion(user_message: str, system_prompt: str) -> str:
    """system_prompt is passed in rather than hardcoded here, so the
    caller (the chat router) decides which mode's prompt to use —
    this is what lets Day 6's comfort/calm toggle slot in cleanly
    without touching this function again.
    """
    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )
    return completion.choices[0].message.content