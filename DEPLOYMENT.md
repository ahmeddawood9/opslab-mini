# Deployment

## Manual Deployment (EC2)

> **Status: pending write-up.** The infrastructure described below is live; this
> section will be filled in with the actual reasoning, commands, and incident
> notes.

### 1. Overview
_TODO — what this is, what it's for._

### 2. Infrastructure decisions
_TODO — AMI/OS choice, instance type, storage size, region, and why for each._

### 3. Security setup
_TODO — IAM user vs. root credentials, policy attached (and the tradeoff),
security group rules, key pair handling._

### 4. The docker.sock permission issue
_TODO — what broke, root cause, the fix used, and why the alternative is an
anti-pattern._

### 5. Docker installation method
_TODO — method used, and why the convenience script was rejected._

### 6. Environment/secrets handling
_TODO — why `.env` isn't committed, and the server-vs-local Postgres password
story._

### 7. Incident: duplicate instance
_TODO — postmortem: what happened, how it was noticed, root cause, resolution,
what would be done differently._

### 8. Verification steps
_TODO — the `curl` commands used to confirm the app was live, internally and
externally._

### 9. Shutdown/cost management
_TODO — stop vs. terminate, and the public-IP-changes-on-restart gotcha._

## CI/CD Pipeline

### CI (GitHub Actions — ci.yml)
- Triggers on `push` and `pull_request` events targeting `main`.
- Runs the test suite (`pytest`) against a throwaway SQLite database.
- Validates the Docker Compose config.
- Builds a Docker image tagged two ways: `latest` (moving pointer) and `sha-<commit-sha>` (immutable, used for rollback).
- On direct pushes to `main` only — guarded by an `if:` condition checking `github.event_name` and `github.ref`, not on PRs — logs into GHCR and pushes both tags.
- Registry: GHCR (`ghcr.io/ahmeddawood9/opslab-mini`), private visibility.
- PRs from forks never get registry write access, by design (security).

### EC2 → GHCR authentication (Phase 2)
- EC2 authenticates to GHCR using a Personal Access Token scoped to `read:packages` only (least privilege).
- Set up via `docker login ghcr.io` with `--password-stdin` (avoids the token landing in shell history).
- Credential is stored in EC2's local Docker config and persists across reboots.
- Verified working via a test `docker pull` of the private image.

### GitHub Actions → EC2 authentication (Phase 3)
- A dedicated SSH keypair (`opslab-cd-key`, ed25519) was generated specifically for CD — separate from the personal login key, so it can be revoked/rotated independently.
- Public key added to EC2's `~/.ssh/authorized_keys` for the `ubuntu` user.
- Private key stored as a GitHub repository secret: `EC2_SSH_KEY`.
- Target host stored as secret `EC2_HOST` (the DuckDNS domain, not a raw IP, since EC2's public IP changes on stop/start).
- SSH user stored as secret `EC2_USER`.

### Known operational notes
- EC2 containers are Docker Compose–managed (`opslab-mini-app-1`, `opslab-mini-db-1`) — deploy commands must use `docker compose` subcommands, not raw `docker run`/`stop`/`rm`.
- EC2 security group restricts SSH (port 22) to a single IP at a time — must be updated manually when connecting from a new network.
- SSH auth is key-only on this instance (`PasswordAuthentication no`, verified via `sshd -T`).

### Not yet implemented
- `cd.yml` workflow itself (triggered via `workflow_run` after CI succeeds) — planned next.
- Deploy sequence: `docker compose pull` + `docker compose up -d`.
- Accepted tradeoff: brief downtime between old and new container during deploy (no rolling/blue-green yet).
