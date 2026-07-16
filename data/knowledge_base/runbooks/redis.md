# Redis Cache Runbook

Product lookup normally has a cache hit rate above 90%.

A sudden hit-rate drop increases database reads and can raise product lookup latency.
Check cache eviction rate, key expiration behavior, Redis memory pressure, and
recent cache-key or TTL changes.
