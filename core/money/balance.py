from app.database import get_balance

def get_user_balance(user_id: int) -> int:
    return get_balance(user_id)
