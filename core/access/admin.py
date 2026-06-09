from config import ADMIN_ID

def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID
