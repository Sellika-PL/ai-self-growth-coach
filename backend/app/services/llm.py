from groq import Groq

from app.config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)

# Placeholder only — replaced with the full reflective Socratic
# sequence in Phase 1, Day 5. Today's goal is just proving the
# wiring works end to end.
PLACEHOLDER_SYSTEM_PROMPT = (
    "You are a supportive assistant for a self-growth app that is still "
    "being built. Keep responses short while this integration is being tested."
)


def get_completion(user_message: str) -> str:
    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": PLACEHOLDER_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    return completion.choices[0].message.content
