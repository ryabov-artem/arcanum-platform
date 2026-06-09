from core.payments.yookassa import create_payment

def buy_spread(user_id: int, count: int, amount: int):
    description = f"Arcanum spreads: {count}"
    return create_payment(amount, description)
