# Deploying to Render

This guide deploys the portfolio demo from the GitHub repository using a Render Blueprint.

## What the Blueprint creates

- **API:** Docker-based FastAPI web service, free instance, health check at `/health`
- **Dashboard:** free static site built from `frontend/`
- **Database:** no database resource is provisioned by default. The API falls back to SQLite for a zero-cost demo.

## Important free-tier behavior

Render free web services spin down after 15 minutes without inbound traffic and can take about a minute to wake. Their local filesystem is ephemeral, so SQLite data can disappear after a restart, spin-down, or redeploy. A free Render Postgres database is limited to 1 GB and expires 30 days after creation; it has no backups. These options are appropriate for a disposable portfolio demonstration, not durable application data or production workloads. Review current [Render free instance limitations](https://render.com/docs/free) before creating services.

**Never send real patient data or PHI to this demo.**

## Deploy steps

1. Push the repository's latest `main` branch to GitHub.
2. Create or sign in to your account at [Render](https://dashboard.render.com/).
3. Choose **New + → Blueprint** and connect the GitHub repository `nVidiaPriyadarshini/healthcare-fhir-quality-platform`.
4. Select the repository and branch `main`. Render detects `render.yaml`; review the two services and approve creation.
5. Wait for the API service to finish deploying. Open its service page and copy its public URL, for example `https://healthcare-fhir-quality-api.onrender.com`.
6. Open the static site service in Render → **Environment**. Set `VITE_API_URL` to the API URL (include `https://`, no trailing slash), then save and redeploy. This is a Vite build-time variable.
7. Open the API URL plus `/health`. Expect JSON similar to `{"status":"ok","fhir_version":"R4"}`.
8. Open the API URL plus `/docs` to inspect Swagger. Open the static site's public URL to check the dashboard.

## CORS configuration

The Blueprint starts with `CORS_ORIGINS=*` so the public portfolio dashboard can call the API. This API has no authentication and is intended only for synthetic demo data. If you later add authentication or non-demo data, replace the wildcard with the exact static-site origin (for example, `https://your-dashboard.onrender.com`) as a comma-separated list.

## Configure durable PostgreSQL later

For a longer-lived demo, create a paid Render Postgres database and set the API service's `DATABASE_URL` environment variable to its **Internal Database URL**, using the SQLAlchemy driver prefix expected by this project: `postgresql+psycopg://...`. Confirm the database URL format and pricing in the Render dashboard before provisioning. Do not put credentials in GitHub or commit them to `render.yaml`. The current free Postgres offering expires after 30 days and is not a durable free database.

## CI and deploy order

GitHub Actions runs backend tests and the frontend production build on pushes and pull requests to `main`. In Render's service settings, set **Auto-Deploy** to **After CI Checks Pass** if that option is available for your GitHub connection; otherwise use **Manual** deploys after confirming the GitHub Actions run is green. Avoid deploying unverified commits.

## Troubleshooting

- **Dashboard says API unavailable:** confirm `VITE_API_URL` is the API's HTTPS URL, save it, and trigger a fresh static-site deploy.
- **Browser CORS error:** confirm the API's `CORS_ORIGINS` includes the exact dashboard origin; save and redeploy the API.
- **First API request is slow:** the free web service may be waking from idle.
- **Records disappeared:** expected with SQLite on an ephemeral free service. Use a paid persistent database if you need records to survive restarts.
- **API deploy fails:** inspect Render service logs; confirm the Docker build context is the repository root and Dockerfile path is `./Dockerfile`.

## Go-live checklist

- [ ] GitHub Actions is green for the deployed commit
- [ ] API `/health` responds successfully
- [ ] API `/docs` opens
- [ ] Dashboard loads and reports a connected API
- [ ] `VITE_API_URL` points to the deployed API
- [ ] No real patient data or secrets are committed
- [ ] README contains the live dashboard and API links (add them after deployment)
