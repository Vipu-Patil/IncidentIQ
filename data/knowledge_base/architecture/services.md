# AgentForge Production Architecture

The platform contains API Gateway, Checkout Service, Payment Service, Order Service,
Inventory Service, Redis Cache, PostgreSQL, and Kafka.

Requests normally flow:
Client -> API Gateway -> Checkout Service -> Payment Service
                                  -> Inventory Service
                                  -> PostgreSQL
                                  -> Redis

Checkout Service is stateless and horizontally scalable. PostgreSQL stores orders,
claims, payment records, and checkout state. Kafka carries asynchronous order events.

Authentication uses OAuth2/JWT at the gateway. Services validate the authenticated
principal and enforce role-based authorization for privileged operations.
