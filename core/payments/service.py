from app.main import create_yookassa_payment

def buy_spread(user_id: int, count: int, amount: int):
    return create_yookassa_payment(user_id, count, amount)
