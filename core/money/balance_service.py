from app.database import get_balance, add_balance, spend_balance

def get(user_id: int) -> int:
    return get_balance(user_id)

def add(user_id: int, amount: int):
    return add_balance(user_id, amount)

def spend(user_id: int):
    return spend_balance(user_id)
