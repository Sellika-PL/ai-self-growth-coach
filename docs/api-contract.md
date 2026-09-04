# API contract

Written before implementation, per Phase 0's architecture-first approach. Every endpoint below maps to a table in `data-model.md`. Implementation (Phase 1+) should match this contract — if it needs to change, update this doc in the same commit as the code change.

All endpoints except `/auth/*` require a valid `Authorization: Bearer <access_token>` header.

## Auth

| Method & path | Request body | Response | Notes |
|---|---|---|---|
| `POST /auth/signup` | `{ email, password }` | `{ access_token, refresh_token }` | Password hashed with argon2 before storage. Rate-limited. |
| `POST /auth/login` | `{ email, password }` | `{ access_token, refresh_token }` | Rate-limited separately from general API limits. |
| `POST /auth/refresh` | `{ refresh_token }` | `{ access_token }` | Refresh token stored as httpOnly secure cookie on the frontend, not localStorage. |

## Conversation

| Method & path | Request body | Response | Notes |
|---|---|---|---|
| `POST /chat` | `{ conversation_id?, message, mode }` | `{ response, conversation_id, crisis_triggered }` | `mode` is `"reflective"` or `"comfort"`. Crisis detector runs before the main model call, on every request. |
| `GET /conversations` | — | `[{ id, mode, started_at }]` | List of the user's past conversations. |
| `GET /conversations/{id}/messages` | — | `[{ role, content, created_at }]` | Full message history for one conversation. |

## Snippet archive

| Method & path | Request body | Response | Notes |
|---|---|---|---|
| `POST /snippets` | `{ content, type, tag }` | snippet object | `type` is `"letter"`, `"script"`, or `"quote"`. |
| `GET /snippets` | — | `[snippet]` | User's own saved snippets. |
| `GET /snippets/resurface?tag=` | — | `snippet \| null` | Only returns a snippet if `consent_resurface` is true for it — enforced in the query, not the frontend. |
| `PATCH /snippets/{id}/consent` | `{ consent_resurface }` | snippet object | Per-item consent toggle. |
| `DELETE /snippets/{id}` | — | `204` | |

## Reflection ledger

| Method & path | Request body | Response | Notes |
|---|---|---|---|
| `GET /ledger/weekly` | — | `{ trend: "less" \| "same" \| "more", visible: bool }` | Returns trend language only, never raw counts — matches the shame-risk mitigation from the scope doc. |
| `PATCH /ledger/visibility` | `{ visible }` | `{ visible }` | Full hide/show toggle for the whole ledger. |

## Account & data controls

| Method & path | Request body | Response | Notes |
|---|---|---|---|
| `GET /users/me/export` | — | full data export (JSON) | Self-service, no support ticket required. |
| `DELETE /users/me` | — | `204` | Full account and data deletion, single action. |

## Deliberately excluded from this contract

No endpoints for Growth Constellations, external wisdom retrieval, or predictive check-ins — those are later-phase additions per `scope.md`.
