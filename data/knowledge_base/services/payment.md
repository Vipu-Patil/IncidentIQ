# Payment Service

Payment Service exposes POST /payments/authorize and POST /payments/capture.

The checkout request waits synchronously for payment authorization. Therefore,
payment-service latency directly contributes to checkout API latency.

Normal p95 authorization latency is below 300 ms. Sustained p95 above 1 second
is considered abnormal.
