from app.database import save_spread

def store_spread(user_id, spread_type, question, cards, answer):
    return save_spread(user_id, spread_type, question, cards, answer)
