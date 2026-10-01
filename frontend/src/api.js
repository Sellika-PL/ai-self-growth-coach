const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

// Matches the /chat contract in docs/api-contract.md: today it's just
// { message, mode } -> { response, mode }. conversation_id and
// crisis_triggered get added once persistence and the safety layer
// land (Days 9+).
export async function sendMessage(message, mode) {
  const res = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, mode }),
  })

  if (!res.ok) {
    throw new Error(`Request failed: ${res.status}`)
  }

  return res.json()
}
