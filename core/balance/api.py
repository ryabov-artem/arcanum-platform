from app.database import get_balance

def user_balance(user_id: int) -> int:
    return get_balance(user_id)

def has_balance(user_id: int) -> bool:
    return get_balance(user_id) > 0
