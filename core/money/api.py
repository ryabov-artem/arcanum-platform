from app.database import add_balance, spend_balance

def add_funds(user_id: int, amount: int):
    return add_balance(user_id, amount)

def charge(user_id: int):
    return spend_balance(user_id)
