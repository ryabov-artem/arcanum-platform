from app.database import get_balance

def get(user_id: int):
    return get_balance(user_id)
