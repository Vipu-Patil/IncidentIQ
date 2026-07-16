# Kafka Consumer Lag Runbook

Order Service consumes order-created events from Kafka.

Healthy consumer lag is normally below 1,000 messages. Rapidly increasing lag
indicates consumers cannot process messages as quickly as producers publish them.

Checks:
- consumer group lag
- consumer error rate
- processing latency
- recent deployment
- partition assignment and rebalance events
