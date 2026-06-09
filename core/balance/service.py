from app.database import spend_balance

def charge_user(user_id: int):
    return spend_balance(user_id)
