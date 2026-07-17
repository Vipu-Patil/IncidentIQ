# Checkout Latency Runbook

For elevated checkout latency:
1. Compare API latency with Payment Service latency.
2. Check database connection-pool utilization.
3. Inspect error and timeout logs.
4. Check Redis hit rate.
5. Compare the incident start time with deployments.
6. Determine whether the problem is isolated to checkout or shared infrastructure.

Do not recommend production rollback solely from a deployment timestamp. Require
supporting evidence.
