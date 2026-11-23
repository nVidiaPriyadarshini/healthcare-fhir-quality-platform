# Setup

## Prerequisites
- Docker Desktop with Docker Compose, or Python 3.11+ and Node.js 20+ for local development.
- Git.

## Run the complete stack with Docker
From the repository root:

```bash
docker compose up --build
```

Compose starts PostgreSQL 16, the FastAPI backend, and the React/Vite dashboard.

- Dashboard: http://localhost:5173
- FastAPI Swagger UI: http://localhost:8000/docs
- API health: http://localhost:8000/health

Stop the stack with `docker compose down`. To also delete the local database volume, use `docker compose down -v` (this permanently removes locally stored demo records).

For shared environments, set a strong `POSTGRES_PASSWORD` in the shell or an environment file before starting Compose. The built-in default is for local development only.

## Load the synthetic FHIR R4 examples
The repository includes fictional Patient, Observation, and Encounter resources in `backend/sample-data/`. From the repository root, load them one at a time:

```bash
curl -X POST http://localhost:8000/api/v1/resources -H "Content-Type: application/json" --data @backend/sample-data/patient.json
curl -X POST http://localhost:8000/api/v1/resources -H "Content-Type: application/json" --data @backend/sample-data/observation.json
curl -X POST http://localhost:8000/api/v1/resources -H "Content-Type: application/json" --data @backend/sample-data/encounter.json
```

A successful ingestion returns the resource ID, type, and quality score. Refresh the dashboard to see the resource inventory and summary metrics. Re-running the same POST requests returns HTTP 409 because duplicate resource IDs are rejected.

To validate a resource without storing it, send its JSON body to `POST /api/v1/validate` using Swagger UI or curl.

## Local development without Docker
### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
```

SQLite is used by default for local development. Set `DATABASE_URL` to a PostgreSQL connection string to use PostgreSQL.

### Frontend
In a second terminal:

```bash
cd frontend
npm install
npm run dev
npm run build
```

Set `VITE_API_URL` if the API is hosted somewhere other than `http://localhost:8000`.

## API endpoints
- `GET /health` — API health and FHIR version.
- `POST /api/v1/validate` — validate a resource and record a validation run.
- `POST /api/v1/resources` — validate and persist a resource.
- `GET /api/v1/resources` — list ingested resources.
- `GET /api/v1/metrics` — dashboard summary metrics.

All included data is synthetic. This starter project is not a certified clinical system or a complete HL7 FHIR R4/profile conformance validator. Do not submit real patient data.
