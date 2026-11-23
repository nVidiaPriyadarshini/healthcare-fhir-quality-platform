# Healthcare FHIR Data Quality & Validation Platform

A synthetic-data-only starter platform for FHIR R4 validation and healthcare data-quality monitoring.

## Stack
- FastAPI, SQLAlchemy and PostgreSQL 16
- FHIR R4-oriented validation rules and quality scoring
- React + TypeScript + Vite dashboard
- Docker Compose and GitHub Actions CI
- Pytest unit and API tests

## Quick start

```bash
docker compose up --build
```

Dashboard: http://localhost:5173 · API: http://localhost:8000 · Swagger: http://localhost:8000/docs

Set `POSTGRES_PASSWORD` in your environment before using any shared deployment. The default is only for local development.

## Tests

```bash
cd backend && pip install -r requirements.txt && pytest -q
cd ../frontend && npm install && npm run build
```

## Synthetic examples

FHIR Patient, Observation and Encounter examples are in `backend/sample-data/`. Submit them to `POST /api/v1/resources`; validate without persistence using `POST /api/v1/validate`.

See [setup documentation](docs/setup.md), [architecture](docs/architecture.md), and the [FHIR data dictionary](docs/data-dictionary.md). Machine-readable starter schemas for Patient, Observation and Encounter are in [`schemas/fhir-r4/`](schemas/fhir-r4/).

**Safety:** all included records are fictional. Do not use real patient data. The starter rules are not a complete HL7 FHIR R4/profile conformance validator or a certified clinical system.
