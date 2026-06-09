from app.database import get_connection

def save_user(user):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO users (user_id, username, first_name, created_at)
    VALUES (?, ?, ?, datetime('now'))
    """, (
        user.id,
        user.username,
        user.first_name
    ))

    conn.commit()
    conn.close()
