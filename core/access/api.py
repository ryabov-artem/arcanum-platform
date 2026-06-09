from core.balance.api import user_balance

def has_paid_access(user_id: int) -> bool:
    return user_balance(user_id) > 0
