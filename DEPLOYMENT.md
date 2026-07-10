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
