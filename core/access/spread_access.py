from core.money.balance_service import get

def has_access(user_id: int) -> bool:
    return get(user_id) > 0
