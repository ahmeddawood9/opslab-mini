1. Overview
What is this, what's it for. One or two sentences.
2. Infrastructure decisions
For each of these, write what you chose and why — the reasoning, not just the value:

AMI / OS choice
Instance type
Storage size
Region

3. Security setup

Why IAM user instead of root credentials for the CLI
What policy you attached, and the tradeoff you'd explain in an interview (broad managed policy vs. scoped custom policy)
Security group rules — what ports, restricted to what, why
Key pair handling — permission mode, where stored

4. The docker.sock permission issue
What broke, what the actual cause was, which fix you used and why the other option is an anti-pattern.
5. Docker installation method
Which method you used, and why you rejected the convenience script despite it being Docker's own recommendation on their homepage.
6. Environment/secrets handling

Why .env isn't committed to git
Why the server's Postgres password differs from your local dev password — include your first wrong answer here too ("I thought it was because IPs were different") and the correction. Don't sanitize your own mistake out of the record — that's the part that actually proves understanding.

7. Incident: duplicate instance
This is the best section — write it like a real postmortem:

What happened (two instances running, one undetected)
How you noticed (describe-instances with the Name tag filter)
Root cause (terminal glitch → command likely sent twice, no describe check before re-running)
Resolution (stop on the duplicate immediately to halt billing, confirmed via timestamp comparison, then terminate since it held nothing)
What you'd do differently next time (check state before re-running a resource-creating command)

8. Verification steps
The curl commands you used to confirm the app was live, both internally and externally.
9. Shutdown/cost management
stop vs terminate, and the fact that stopping changes the public IP on restart.

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
