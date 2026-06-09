from app.database import (
    save_payment,
    get_recent_payments,
    get_payments_stats,
    get_sales_funnel
)

def save(payment_id, user_id, amount, spreads_added):
    return save_payment(payment_id, user_id, amount, spreads_added)

def recent(limit=10):
    return get_recent_payments(limit)

def stats():
    return get_payments_stats()

def funnel():
    return get_sales_funnel()
