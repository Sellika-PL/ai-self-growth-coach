# Tech stack decisions

Each choice below is made against three constraints: $0 cost, buildable by a solo/small student team, and no vendor lock-in that would block a later migration.

## Frontend — React + Vite

- **Why:** Vite gives a fast dev server and simple build step; React is the most widely documented option, which matters for a first solo project where getting unstuck quickly matters more than picking the "best" framework.
- **Alternative considered:** plain HTML/JS. Rejected — the chat UI's state (messages, mode toggle, ledger view) is exactly the kind of thing component state is built for.

## Backend — FastAPI + SQLModel

- **Why:** FastAPI gives automatic request validation and API docs for free (the OpenAPI schema doubles as living documentation of the API contract from Day 3). SQLModel (built on SQLAlchemy + Pydantic) means the same model class defines both the database table and the API request/response shape — less duplication for a solo developer to keep in sync.
- **Alternative considered:** Flask + raw SQLAlchemy. Rejected — more boilerplate for validation, which matters more here than usual since this app handles sensitive personal data and validation gaps are a real risk, not just a convenience issue.

## Database — SQLite (dev) → Postgres via Supabase/Neon (prod)

- **Why:** SQLite needs zero setup for local development. Supabase and Neon both offer genuinely free Postgres tiers with encryption at rest included, so the production database costs nothing and the schema is portable between the two (both are real Postgres, not a proprietary variant).
- **Alternative considered:** staying on SQLite in production. Rejected — SQLite doesn't handle concurrent writes well, and a real Postgres instance from day one avoids a migration later.

## LLM inference — Groq free tier

- **Why:** no credit card required, no expiry, generous free rate limits, and it serves genuinely capable open-weight models (Llama 3.x family). This is the choice that keeps the whole project at $0 without needing to train a model from scratch, which isn't feasible at this scale.
- **Known limitation:** rate limits (per-minute and per-day request caps) are real — fine for development and a small validation group, but a future constraint if the app gets real traction. Not a blocker for the MVP.
- **Alternative considered:** self-hosting an open model via Ollama in production. Rejected for production (would need a paid always-on server with enough RAM/CPU) but kept as the recommended path for local development and offline testing, since Ollama is fully free and requires no external API calls at all.

## Hosting — Render/Fly.io (backend) + GitHub Pages/Vercel (frontend)

- **Why:** all four have real $0 tiers that include HTTPS by default, which matters — encryption in transit is non-negotiable for an app handling personal reflections, and these platforms give it for free rather than requiring manual TLS setup.
- **Alternative considered:** AWS free tier. Rejected as the default — AWS's free tier is time-limited (mostly 12 months) and can silently start billing after that or if usage is miscalculated. Kept as a deliberate, separate learning exercise later (see the roadmap's cloud-fundamentals module), using Oracle Cloud's Always Free tier instead for anything meant to stay genuinely free indefinitely.

## CI — GitHub Actions

- **Why:** free minutes are included on every GitHub repo, and it's the natural fit for the branch-per-phase workflow already in use — tests and linting run automatically on every push, without needing a separate CI account.
