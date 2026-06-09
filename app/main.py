import asyncio
from core.access.api import has_paid_access
from core.users.api import register_user
import os
import uuid
import re

from ai import (
    interpret_day_card,
    interpret_three_cards,
    interpret_relationship_spread,
    interpret_career_spread,
    interpret_money_spread
)

from core.database.api import (
    init_db,
    get_today_card,
    save_daily_card,
    save,
    get_user_spreads,
    get_users_count,
    get_daily_cards_count,
    get_spreads_count,
    get_recent_spreads,
    get_recent_users,
    get_spread_type_stats,
    get_recent_payments,
    get_payments_stats,
    get_sales_funnel,
    get_top_users,
    get_all_user_ids,
    can_use_free_spread,
    mark_free_spread_used,
    charge,
    add_funds
)

from tarot import draw_card, draw_three_cards

from aiogram import Bot, Dispatcher, F
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from core.payments.yookassa import create_payment

load_dotenv("/opt/bots/tarot_bot/.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
PROXY_URL = os.getenv("PROXY_URL")
PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")
YOOKASSA_SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
YOOKASSA_SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")
YOOKASSA_RETURN_URL = os.getenv("YOOKASSA_RETURN_URL")

if YOOKASSA_SHOP_ID and YOOKASSA_SECRET_KEY:
    Configuration.account_id = YOOKASSA_SHOP_ID
    Configuration.secret_key = YOOKASSA_SECRET_KEY

ADMIN_ID = 185955220

session = AiohttpSession(proxy=PROXY_URL)
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()

awaiting_three_card_question = set()
awaiting_relationship_question = set()
awaiting_career_question = set()
awaiting_money_question = set()
awaiting_broadcast_text = set()
pending_broadcast = {}


def markdown_bold_to_html(text):
    return re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)


def get_main_keyboard(user_id):
    keyboard = [
        [KeyboardButton(text="🎁 Карта дня"), KeyboardButton(text="🌟 Общий расклад")],
        [KeyboardButton(text="❤️ Отношения"), KeyboardButton(text="💼 Карьера")],
        [KeyboardButton(text="💰 Деньги"), KeyboardButton(text="💎 Баланс")],
        [KeyboardButton(text="📜 История"), KeyboardButton(text="ℹ️ О боте")]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👥 Пользователи")],
        [KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="💰 Платежи")],
        [KeyboardButton(text="📜 Последние расклады")],
        [KeyboardButton(text="📊 Популярность")],
        [KeyboardButton(text="📣 Рассылка")],
        [KeyboardButton(text="🎁 Акции")],
        [KeyboardButton(text="📈 Воронка")],
        [KeyboardButton(text="🏆 Топ")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)




shop_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🪙 Купить 1 расклад — 99 ₽")],
        [KeyboardButton(text="💎 Купить 5 раскладов — 299 ₽")],
        [KeyboardButton(text="🔮 Купить 10 раскладов — 499 ₽")],
        [KeyboardButton(text="👑 Купить 20 раскладов — 799 ₽")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)


broadcast_confirm_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Отправить"), KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True
)


promo_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎁 Акция: 5 раскладов")],
        [KeyboardButton(text="🔮 Напомнить про карту дня")],
        [KeyboardButton(text="💰 Скидка на расклады")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)




def user_has_spread_access(user_id):
    if can_use_free_spread(user_id):
        return True

    if core.access.api.has_paid_access(user_id):
        return True

    return False

    if core.access.api.has_paid_access(user_id):
        return True

    return False

def charge_user_for_spread(user_id):
