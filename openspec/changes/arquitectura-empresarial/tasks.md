# Tasks: Upgrade a Arquitectura Empresarial (FastAPI + React)

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 600-800 lines |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 (Backend FastAPI) → PR 2 (Frontend React) |
| Delivery strategy | ask-on-risk |
| Chain strategy | stacked-to-main |

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: stacked-to-main
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Backend API with FastAPI and LangChain agent | PR 1 | Base branch: main; returns critical stock and chats with agent |
| 2 | Frontend Dashboard and Copiloto Chat | PR 2 | Base branch: main (or PR 1); Vite React app using Vanilla CSS |

## Phase 1: Backend Foundation
- [x] 1.1 Create `backend/` directory and move `src/` to `backend/src/`.
- [x] 1.2 Create `backend/main.py` with FastAPI initialization and CORS middleware.
- [x] 1.3 Update paths in `backend/src/config/settings.py` to support `backend/` directory structure.

## Phase 2: FastAPI Endpoints
- [x] 2.1 Implement `GET /api/inventory/critical` returning low-stock items from SQLite.
- [x] 2.2 Implement `POST /api/agent/chat` routing conversations to `InventoryAgent` and returning responses.
- [x] 2.3 Add startup event to `main.py` verifying ChromaDB vector store and SQLite database accessibility.

## Phase 3: Frontend Bootstrap
- [ ] 3.1 Initialize React/Vite app in `frontend/` using `npx -y create-vite@latest frontend --template react`.
- [ ] 3.2 Configure CSS variables, dark mode styling, and responsive layout in `frontend/src/index.css`.
- [ ] 3.3 Create client API fetch utilities in `frontend/src/services/api.js`.

## Phase 4: Frontend Components
- [ ] 4.1 Create `Sidebar` component showing logo, connection status, and navigation.
- [ ] 4.2 Create `KPICards` component displaying total products, critical alert counts, and averages.
- [ ] 4.3 Create `AgentChat` component with messages history, typing indicators, and user input.

## Phase 5: Verification & Cleanup
- [ ] 5.1 Verify backend APIs using curl/pytest, checking chat flow fallback and SQLite queries.
- [ ] 5.2 Remove obsolete files: root-level `app.py` (Streamlit).
- [ ] 5.3 Update root `README.md` with startup instructions for FastAPI backend and React frontend.
