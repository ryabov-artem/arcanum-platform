from core.users.repository import save_user
from app.database import get_users_count, get_all_user_ids, get_recent_users

def register_user(user):
    return save_user(user)

def users_count():
    return get_users_count()

def all_user_ids():
    return get_all_user_ids()

def recent_users(limit=10):
    return get_recent_users(limit)
