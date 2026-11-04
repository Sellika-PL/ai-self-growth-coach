import { useState } from 'react'
import { sendMessage } from './api'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [mode, setMode] = useState('reflective')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSend(e) {
    e.preventDefault()
    const text = input.trim()
    if (!text || loading) return

    // Add the user's message immediately -- don't wait for the
    // network round trip before showing what they typed.
    setMessages((prev) => [...prev, { role: 'user', content: text }])
    setInput('')
    setLoading(true)
    setError(null)

    try {
      const data = await sendMessage(text, mode)
      setMessages((prev) => [...prev, { role: 'assistant', content: data.response }])
    } catch (err) {
      setError('Could not reach the server. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>AI Self-Growth Coach</h1>
        <div className="mode-toggle" role="group" aria-label="Conversation mode">
          <button
            type="button"
            className={mode === 'reflective' ? 'active' : ''}
            onClick={() => setMode('reflective')}
          >
            Reflective
          </button>
          <button
            type="button"
            className={mode === 'comfort' ? 'active' : ''}
            onClick={() => setMode('comfort')}
          >
            Just listen
          </button>
        </div>
      </header>

      <main className="messages">
        {messages.length === 0 && (
          <p className="empty-state">What's on your mind today?</p>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.role}`}>
            {m.content}
          </div>
        ))}
        {loading && <div className="message assistant loading">…</div>}
        {error && <div className="message error">{error}</div>}
      </main>

      <form className="composer" onSubmit={handleSend}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type here..."
          aria-label="Message"
        />
        <button type="submit" disabled={loading}>
          Send
        </button>
      </form>
    </div>
  )
}

export default App
