from app.database import (
    get_spread_type_stats,
    get_sales_funnel,
    get_top_users,
    get_daily_cards_count,
    get_spreads_count
)

def stats():
    return {
        "spread_type": get_spread_type_stats(),
        "sales_funnel": get_sales_funnel(),
        "top_users": get_top_users(),
        "daily_cards": get_daily_cards_count(),
        "spreads": get_spreads_count(),
    }
