from yookassa import Configuration, Payment

def create_payment(amount: int, description: str):
    payment = Payment.create({
        "amount": {
            "value": str(amount),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/"
        },
        "capture": True,
        "description": description
    })

    return payment.confirmation.confirmation_url
