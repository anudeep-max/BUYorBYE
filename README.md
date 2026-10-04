# BUYorBYE

Minimal local application foundation with a **React + Vite + TypeScript** frontend and a **Python + FastAPI** backend. The temporary page displays **“BUYorBYE is running.”** and checks the backend's health endpoint.

No Gemini integration, web search, product/food comparisons, or authentication is implemented.

## Project structure

```text
BUYorBYE/
├── frontend/
│   ├── src/                 # React UI
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── backend/
│   ├── app/
│   │   └── main.py          # FastAPI app and GET /health
│   ├── tests/               # Health and CORS checks
│   ├── requirements.txt
│   └── requirements-dev.txt
├── .env.example
└── README.md
```

The frontend and backend have independent dependencies and run in separate terminals. There is no root application package or combined server.

## Prerequisites

- Node.js **20.19+ (20.x)** or **22.12+** and npm.
- Python **3.10+**, pip, and the standard-library `venv` module.

## 1. Configure the environment

From the repository root:

```bash
cp .env.example .env
```

Both apps read this root `.env`; no separate copies in `frontend/` or `backend/` are needed. Defaults also allow the applications to run without a `.env` file.

| Variable | Purpose | Default |
| --- | --- | --- |
| `VITE_API_BASE_URL` | Backend URL used by the frontend | `http://127.0.0.1:8000` |
| `CORS_ORIGINS` | Comma-separated browser origins allowed by FastAPI | `http://localhost:5173,http://127.0.0.1:5173` |

`VITE_` variables are public and included in the frontend bundle. Never place secrets in them. `.env` is ignored by Git. Backend shell environment variables take precedence over `.env`.

## 2. Run the backend

In your first terminal, starting from the repository root:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

On Windows, use `python` instead of `python3` to create the environment, and activate it with `.venv\Scripts\Activate.ps1` in PowerShell.

- Backend: <http://127.0.0.1:8000>
- Health check: <http://127.0.0.1:8000/health>
- FastAPI API docs: <http://127.0.0.1:8000/docs>

The backend root `/` is intentionally not an application page. `GET /health` returns HTTP 200 with:

```json
{"status": "ok"}
```

## 3. Run the frontend

In a second terminal, starting from the repository root:

```bash
cd frontend
npm ci
npm run dev
```

Open <http://127.0.0.1:5173>. You should see:

```text
BUYorBYE is running.
Backend connected.
```

If the backend is not running or cannot be reached, the page still loads and displays a backend-unavailable message. Start the backend and refresh the page.

### Port conflicts and environment changes

Vite uses a strict port so it cannot silently switch ports and break CORS. If port `5173` is occupied, either stop the process you own on that port or choose another explicitly:

```bash
npm run dev -- --port 5174
```

For port `5174`, also add `http://127.0.0.1:5174` (and `http://localhost:5174` if used) to `CORS_ORIGINS` in the root `.env`. Restart the backend after changing its environment. Restart Vite after changing frontend environment variables.

If you change the backend port, update `VITE_API_BASE_URL` accordingly. Browser origins must match their scheme, hostname, and port exactly; do not add paths or trailing slashes to `CORS_ORIGINS`. CORS permits the configured origins, without credentialed requests.

## Checks

Frontend typecheck and production build:

```bash
cd frontend
npm run typecheck
npm run build
```

Backend health and CORS regression checks, with the backend virtual environment active:

```bash
cd backend
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

Live health check while the backend is running:

```bash
curl http://127.0.0.1:8000/health
```

To preview the frontend production build, run `npm run preview` inside `frontend/` after building. This uses <http://127.0.0.1:4173>; add that origin to `CORS_ORIGINS` and restart the backend if you want the preview to reach `/health`.
