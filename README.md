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
- SQLite local persistence
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

## Rule

No real secrets, credentials, tokens, private keys, or cloud resources are committed.
