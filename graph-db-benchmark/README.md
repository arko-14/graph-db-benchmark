# Graph DB Benchmark

Copy `.env.example` to `.env` for local development. The `.env` file is intentionally ignored by git, so keep secrets and machine-specific ports there and commit only `.env.example` updates.

If Docker Compose fails with `Bind for 0.0.0.0:7687 failed: port is already allocated`, another container is already using Neo4j's default Bolt port.

Set a different host port in `.env` before starting the stack:

```env
NEO4J_BOLT_PORT=7689
NEO4J_URI=bolt://localhost:7689
```

Then start the services again with `docker compose up -d`.
