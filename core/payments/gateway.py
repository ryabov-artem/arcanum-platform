from yookassa import Configuration, Payment

def create_payment(user_id: int, count: int, amount_rub: int):
    payment = Payment.create({
        "amount": {
            "value": str(amount_rub),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/your_bot"
        },
        "capture": True,
        "description": f"Arcanum spreads: {count}"
    })

    return payment
