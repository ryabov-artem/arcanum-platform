from app.database import save_spread, get_user_spreads, get_recent_spreads

def save(user_id, spread_type, question, cards, answer):
    return save_spread(user_id, spread_type, question, cards, answer)

def user_history(user_id, limit=5):
    return get_user_spreads(user_id, limit)

def recent(limit=10):
    return get_recent_spreads(limit)
