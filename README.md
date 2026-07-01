# opslab-mini

A small FastAPI service used as a DevOps learning target.

The app simulates internal platform events such as deployments, errors, and heartbeats. The goal is to use this service for hands-on Docker, CI/CD, deployment, monitoring, and infrastructure practice.

## Why this exists

Most DevOps learning becomes abstract because there is no real app to run, break, deploy, or observe.

This project gives me a small backend system that can be used to practice:

- containerization
- service health checks
- CI pipelines
- deployment workflows
- logging and monitoring
- environment-based configuration
- production-style debugging

## Current scope

- FastAPI backend
- SQLite by default, with PostgreSQL available through Docker Compose
- Health and readiness endpoints
- Event creation and listing
- Admin endpoints for simulating errors and latency
- Basic tests with pytest

## API endpoints

- `GET /health/live`
- `GET /health/ready`
- `GET /version`
- `POST /events`
- `GET /events`
- `GET /events/{id}`
- `POST /admin/simulate-error`
- `POST /admin/simulate-latency?seconds=2`

## Docker Compose local development

Required setup:

```bash
cp .env.example .env
```

Review `.env` before starting the stack. The included values are local development examples only.

Validate the Compose file:

```bash
docker compose config
```

Start the API and PostgreSQL:

```bash
docker compose up --build
```

Check logs:

```bash
docker compose logs -f app
docker compose logs -f db
```

Stop containers:

```bash
docker compose down
```

Reset the PostgreSQL data volume only when you intentionally want to delete local database data:

```bash
docker compose down -v
```

The app connects to PostgreSQL at `db:5432` because `db` is the Compose service name on the internal Docker network. Do not use `localhost` from inside the app container; inside that container, `localhost` means the app container itself.

## Rule

No real secrets, credentials, tokens, private keys, or cloud resources are committed.
