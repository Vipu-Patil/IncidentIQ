# PostgreSQL Database Runbook

Checkout uses a PostgreSQL connection pool. The normal pool configuration is:
maximum connections per application pod: 40
minimum idle connections: 5
connection acquisition timeout: 2 seconds.

Symptoms of pool exhaustion:
- connection acquisition timeout
- rising request latency
- low CPU despite high API latency
- logs containing "pool exhausted" or "timeout acquiring connection"

First checks:
1. Inspect application pool utilization.
2. Check active PostgreSQL sessions.
3. Check slow queries.
4. Check whether a recent release changed transaction handling.
