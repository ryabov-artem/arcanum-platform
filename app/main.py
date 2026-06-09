import asyncio
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
from core.users.api import register_user
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
    core.access.api.has_paid_access,
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

    if from core.access.admin import is_admin:
        keyboard.append([KeyboardButton(text="⚙️ Админка")])

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


    if can_use_free_spread(user_id):
        return True

    if core.access.api.has_paid_access(user_id) > 0:
        return True

    return False


def charge_user_for_spread(user_id):
    if can_use_free_spread(user_id):
        mark_free_spread_used(user_id)
    elif core.access.api.has_paid_access(user_id) > 0:
        charge(user_id)


async def no_access_message(message: Message):
    await message.answer(
        "💎 Бесплатный расклад уже использован.\n\n"
        "Чтобы продолжить, пополните баланс раскладов.\n\n"
        "Доступные пакеты:\n"
        "🪙 1 расклад — 99 ₽\n"
        "💎 5 раскладов — 299 ₽\n"
        "🔮 10 раскладов — 499 ₽\n"
        "👑 20 раскладов — 799 ₽\n\n"
        "1 расклад = 1 подробный ответ карт.\n\n"
        "Пока можете пользоваться бесплатной картой дня 🎁"
    )


@dp.message(CommandStart())
async def start(message: Message):
    register_user(message.from_user)

    await message.answer(
        "🔮 Арканум\n\n"
        "Добро пожаловать.\n\n"
        "Карты Таро помогут взглянуть на ситуацию под новым углом и получить глубокую интерпретацию вашего вопроса.\n\n"
        "✨ Бесплатно каждый день:\n"
        "• Карта дня\n\n"
        "🔮 Доступные расклады:\n"
        "• Общий\n"
        "• Отношения\n"
        "• Карьера\n"
        "• Деньги\n\n"
        f"💎 Ваш баланс: {core.access.api.has_paid_access(message.from_user.id)} расклад(ов)\n\n"
        "Выберите действие ниже 👇",
        reply_markup=get_main_keyboard(message.from_user.id)
    )



@dp.message(F.text.startswith("/give"))
async def admin_give_balance(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Нет доступа.")
        return

    parts = message.text.split()

    if len(parts) != 3:
        await message.answer(
            "Формат команды:\n"
            "/give USER_ID COUNT\n\n"
            "Пример:\n"
            "/give 185955220 5"
        )
        return

    try:
        target_user_id = int(parts[1])
        amount = int(parts[2])
    except ValueError:
        await message.answer("USER_ID и COUNT должны быть числами.")
        return

    if amount <= 0:
        await message.answer("COUNT должен быть больше 0.")
        return

    add_funds(target_user_id, amount)

    await message.answer(
        f"✅ Начислено {amount} расклад(ов).\n"
        f"Пользователь: {target_user_id}"
    )

    try:
        await bot.send_message(
            chat_id=target_user_id,
            text=(
                f"💎 Тебе начислено {amount} расклад(ов).\n\n"
                "Можешь использовать их в любом платном раскладе."
            )
        )
    except Exception:
        pass


@dp.message(F.text == "🎁 Карта дня")
async def day_card(message: Message):
    register_user(message.from_user)

    existing_card = get_today_card(message.from_user.id)

    if existing_card:
        await message.answer(
            f"🔮 <b>Ваша карта дня уже открыта</b>\n\n"
            f"🎴 <b>{existing_card['name']}</b>\n"
            f"Положение: {existing_card['orientation']}\n\n"
            f"{markdown_bold_to_html(existing_card['interpretation'])}\n\n"
            f"✨ Новая карта будет доступна завтра.",
            parse_mode="HTML"
        )
        return

    card = draw_card()

    await message.answer("🃏 Перемешиваю колоду...")

    interpretation = interpret_day_card(card)

    save_daily_card(message.from_user.id, card, interpretation)

    photo = FSInputFile(f"/opt/bots/tarot_bot/data/cards/{card['image']}")

    await message.answer_photo(
        photo=photo,
        caption=(
            f"🔮 <b>Карта дня</b>\n\n"
            f"🎴 <b>{card['name']}</b>\n"
            f"Положение: {card['orientation']}\n\n"
            f"{markdown_bold_to_html(interpretation)}\n\n"
            f"✨ Пусть эта подсказка поможет пройти день внимательнее."
        ),
        parse_mode="HTML"
    )


@dp.message(F.text == "💎 Баланс")
async def balance(message: Message):
    register_user(message.from_user)

    balance_count = core.access.api.has_paid_access(message.from_user.id)

    await message.answer(
        f"💎 Ваш баланс\n\n"
        f"Доступно раскладов: {balance_count}\n\n"
        f"🔮 Один расклад = один подробный ответ карт.\n\n"
        f"Доступные пакеты:\n"
        f"🪙 1 расклад — 99 ₽\n"
        f"💎 5 раскладов — 299 ₽\n"
        f"🔮 10 раскладов — 499 ₽\n"
        f"👑 20 раскладов — 799 ₽\n\n"
        f"Выберите подходящий вариант ниже 👇",
        reply_markup=shop_keyboard
    )





@dp.message(F.text.contains("Купить 1 расклад"))

async def buy_one_spread(message: Message):
    from core.payments.service import buy_spread
    payment = buy_spread(message.from_user.id, 1, 99)
    url = payment.confirmation.confirmation_url
    await message.answer(f"Оплатите расклад: {url}")

async def buy_five_spreads(message: Message):
    from core.payments.service import buy_spread
    payment = buy_spread(message.from_user.id, 5, 299)
    url = payment.confirmation.confirmation_url
    await message.answer(f"Оплатите 5 раскладов: {url}")


async def buy_ten_spreads(message: Message):
    from core.payments.service import buy_spread
    payment = buy_spread(message.from_user.id, 10, 499)
    url = payment.confirmation.confirmation_url
    await message.answer(f"Оплатите 10 раскладов: {url}")


async def buy_twenty_spreads(message: Message):
    from core.payments.service import buy_spread
    payment = buy_spread(message.from_user.id, 20, 799)
    url = payment.confirmation.confirmation_url
    await message.answer(f"Оплатите 20 раскладов: {url}")
