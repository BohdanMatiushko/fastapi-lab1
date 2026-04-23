from prometheus_client import Counter, Gauge

TOTAL_REVENUE = Counter(
    "total_revenue_dollars",
    "Total revenue in dollars from all order items created"
)

TOTAL_ORDERS = Counter(
    "total_orders_created",
    "Total number of orders created"
)

ACTIVE_USERS = Gauge(
    "active_users_current",
    "Number of active users (mocked/example)"
)
