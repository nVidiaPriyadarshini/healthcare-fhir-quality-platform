# Setup
## Docker
Run `docker compose up --build` from the repository root. API docs: http://localhost:8000/docs. Start frontend separately: `cd frontend && npm install && npm run dev`; dashboard: http://localhost:5173. Compose starts PostgreSQL and FastAPI. Change POSTGRES_PASSWORD for shared environments.
## Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
```
SQLite is the local default; set DATABASE_URL for PostgreSQL.
## Frontend
```bash
cd frontend && npm install && npm run dev && npm run build
```
Set VITE_API_URL if the API is hosted elsewhere.
## Synthetic samples
Submit JSON files in backend/sample-data to POST /api/v1/resources. Use POST /api/v1/validate for validation without persistence.
## Endpoints
GET /health; POST /api/v1/validate; POST /api/v1/resources; GET /api/v1/resources; GET /api/v1/metrics.
All data is synthetic. This is a demonstration, not a certified clinical system.
