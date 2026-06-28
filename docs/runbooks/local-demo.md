# Local Demo Runbook

1. copy .env.example .env

2. docker compose up --build

3. Test with the commands in docs/local-development.md

To debug:
docker compose logs maf-orchestrator

For state, set USE_COSMOS_STATE=false for in-mem, or run Cosmos emulator separately.

No Azure deploys.
