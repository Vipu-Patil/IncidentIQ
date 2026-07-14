# Checkout Service

Checkout handles cart validation, inventory reservation, payment authorization,
and order creation. It exposes POST /checkout and GET /checkout/{id}.

Synchronous dependencies are Payment Service, Inventory Service, and PostgreSQL.
Redis is used for short-lived product and cart metadata.

Checkout is written in Python and deployed as Kubernetes pods. Each pod has its own
database connection pool.
