# Memory Pressure Runbook

Checkout pods normally use less than 600 MiB. Sustained growth toward the
1 GiB container limit can cause Kubernetes OOMKilled restarts.

Checks:
- container memory over time
- restart count
- heap/object growth
- recent code deployment
- whether memory falls after pod restart

Do not infer a memory leak from one high-memory sample; look for sustained growth.
