from app.database import get_spread_type_stats, get_top_users

def spread_stats():
    return get_spread_type_stats()

def top_users(limit=10):
    return get_top_users(limit)
