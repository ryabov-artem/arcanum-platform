import os
import httpx
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("/opt/bots/tarot_bot/.env")

PROXY_URL = os.getenv("PROXY_URL")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    http_client=httpx.Client(
        proxy=PROXY_URL,
        timeout=60.0
    )
)

def interpret_day_card(card):
    prompt = f"""
Ты — AI-ассистент для развлекательных и рефлексивных раскладов Таро.

Правила:
- Не предсказывай будущее как факт.
- Не используй запугивание.
- Не давай медицинских, юридических и финансовых советов.
- Пиши на русском языке.
- Используй эмодзи.
- Не более 120 слов.\n- Используй Telegram HTML для форматирования: <b>жирный текст</b>.\n- Не используй Markdown: **жирный**, ###, ```.

Карта:
{card["name"]} ({card["orientation"]})

Сделай красивую интерпретацию карты дня.
"""

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )

    return response.output_text


def interpret_three_cards(question, cards):
    cards_text = "\n".join(
        [
            f"{i+1}. {card['name']} ({card['orientation']})"
            for i, card in enumerate(cards)
        ]
    )

    prompt = f"""
Ты — AI-ассистент для развлекательных раскладов Таро.

Важно:
- Не предсказывай будущее как факт.
- Не используй запугивание.
- Не давай медицинских, юридических и финансовых советов.
- Пиши на русском языке.
- Используй эмодзи.
- Не более 250 слов.
- Используй Telegram HTML для форматирования: <b>жирный текст</b>.
- Не используй Markdown: **жирный**, ###, ```.

Вопрос:
{question}

Карты:
{cards_text}

Формат ответа строго с HTML-заголовками:

<b>🔮 Общий настрой</b>

<b>1️⃣ Суть ситуации</b>

<b>2️⃣ Скрытый фактор</b>

<b>3️⃣ Возможное направление</b>

<b>💡 Совет карт</b>
"""

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )

    return response.output_text

def interpret_relationship_spread(question, cards):
    cards_text = "\n".join(
        [
            f"{i+1}. {card['name']} ({card['orientation']})"
            for i, card in enumerate(cards)
        ]
    )

    prompt = f"""
Ты — AI-ассистент для развлекательных и рефлексивных раскладов Таро.

Важно:
- Не предсказывай будущее как факт.
- Не используй запугивание.
- Не давай медицинских, юридических и финансовых советов.
- Пиши на русском языке.
- Используй эмодзи.
- Не более 280 слов.
- Используй Telegram HTML для форматирования: <b>жирный текст</b>.
- Не используй Markdown: **жирный**, ###, ```.

Это расклад на отношения.

Вопрос пользователя:
{question}

Выпавшие карты:
{cards_text}

Формат ответа строго с HTML-заголовками:

<b>❤️ Чувства</b>
Что может происходить на эмоциональном уровне.

<b>🔍 Скрытые факторы</b>
Что может быть неочевидно.

<b>➡️ Динамика</b>
Куда ситуация может двигаться при текущих тенденциях.

<b>💡 Совет карт</b>
Мягкий практический вывод для пользователя.
"""

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )

    return response.output_text

def interpret_career_spread(question, cards):
    cards_text = "\n".join(
        [
            f"{i+1}. {card['name']} ({card['orientation']})"
            for i, card in enumerate(cards)
        ]
    )

    prompt = f"""
Ты — AI-ассистент для развлекательных и рефлексивных раскладов Таро.

Важно:
- Не предсказывай будущее как факт.
- Не давай финансовых рекомендаций.
- Не обещай прибыль.
- Пиши на русском языке.
- Используй эмодзи.
- Не более 280 слов.
- Используй Telegram HTML для форматирования: <b>жирный текст</b>.
- Не используй Markdown: **жирный**, ###, ```.

Это расклад на карьеру и работу.

Вопрос пользователя:
{question}

Выпавшие карты:
{cards_text}

Формат ответа строго с HTML-заголовками:

<b>💼 Работа</b>
Что происходит в профессиональной сфере.

<b>📈 Возможности</b>
На что стоит обратить внимание.

<b>⚠️ Риски</b>
Что может тормозить развитие.

<b>💡 Совет карт</b>
Практический вывод для размышления.
"""

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )

    return response.output_text

def interpret_money_spread(question, cards):
    cards_text = "\n".join(
        [
            f"{i+1}. {card['name']} ({card['orientation']})"
            for i, card in enumerate(cards)
        ]
    )

    prompt = f"""
Ты — AI-ассистент для развлекательных и рефлексивных раскладов Таро.

Важно:
- Не предсказывай будущее как факт.
- Не давай инвестиционных советов.
- Не обещай прибыль.
- Не рекомендуй кредиты, займы или финансовые продукты.
- Пиши на русском языке.
- Используй эмодзи.
- Не более 280 слов.
- Используй Telegram HTML для форматирования: <b>жирный текст</b>.
- Не используй Markdown: **жирный**, ###, ```.

Это расклад на деньги и финансовую сферу.

Вопрос пользователя:
{question}

Выпавшие карты:
{cards_text}

Формат ответа строго с HTML-заголовками:

<b>💰 Финансовая ситуация</b>
Что может происходить сейчас.

<b>📈 Возможности</b>
Где могут быть точки роста.

<b>⚠️ Ограничения</b>
Что может мешать.

<b>💡 Совет карт</b>
Осторожный вывод для размышления.
"""

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )

    return response.output_text
